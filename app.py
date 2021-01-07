import os
import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home_page")
def home_page():
    expenses = mongo.db.expenses.find().sort("date", -1)
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("index.html", expenses=expenses, categories=categories)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})
        existing_email = mongo.db.users.find_one({"email_address": request.form.get("email").lower()})

        # check whether user already exists
        if existing_user:
            flash("User already exists")
            return redirect(url_for("register"))
        
        # check whether e-mail address was already used to sign up
        if existing_email:
            flash("An account already exists for this e-mail address!")
            return redirect(url_for("register"))
        
        create_account = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email_address": request.form.get("email").lower(),
            "is_superuser": False
        }
        mongo.db.users.insert_one(create_account)

        session["user"] = request.form.get("username").lower()
        flash("Registration successful!")
        return redirect(url_for("home_page", username=session["user"]))

    return render_template("register.html")


@app.route("/update_profile/<username>", methods=["GET", "POST"])
def update_profile(username):
    if request.method == "POST":
        is_superuser = True if mongo.db.users.find_one(
            {"username": username,
            "is_superuser": True}) else False
        updated_account = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email_address": request.form.get("email").lower(),
            "is_superuser": is_superuser
        }
        mongo.db.users.update({"username": username}, updated_account)

        session["user"] = request.form.get("username").lower()
        flash("Your profile was successfully updated")
        return redirect(url_for("profile", username=username))

    return render_template("update_profile.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})    
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    return redirect(url_for(
                        "home_page", username=session["user"]))

            else:
                # invalid password match
                flash("Invalid login credentials!")
                return redirect(url_for("login"))

        else: 
            # username doesn't exist
            flash("Invalid login credentials!")
            return redirect(url_for("login"))

    return render_template("login.html")    


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("home_page"))


@app.route("/profile/<username>")
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    categories = mongo.db.categories.find().sort("category_name", 1)
    
    if session["user"]:
        return render_template("profile.html", username=username, categories=categories)
    
    return redirect(url_for("login"))


@app.route("/set_budgets/<category_id>", methods=["GET", "POST"])
def set_budgets(category_id):
    if request.method == "POST":
        budget = {
            "category_name": request.form.get("category_name"),
            "budget_amount": float(request.form.get("budget_amount")),
            "created_by": session["user"]
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, budget)
        flash("Budget set successfully")
    
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]    
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    expenses = mongo.db.expenses.find()
    return render_template("profile.html", category=category, categories=categories, expenses=expenses)

@app.route("/calculate_remaining_budgets/<category_id>")
def calculate_remaining_budgets(category_id, expense_id):
    categories = mongo.db.categories.find()
    expenses = mongo.db.expenses.find()

    zipped_data = zip(expenses, categories)
    for expense, category in zipped_data:
        remaining_budget = {
            "category_name": request.form.get("category_name"),
            "budget_amount": float(request.form.get("budget_amount")),
            "remaining_budget": float(category.budget_amount - expense.expense_amount)
        }
        mongo.db.categories.update_one({"_id": ObjectId(category_id)}, remaining_budget)
        return redirect(url_for("calculate_remaining_budgets"))
    
    return render_template("profile.html", expenses=expenses, categories=categories)


@app.route("/my_expenses/<username>")
def my_expenses(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    expenses = list(mongo.db.expenses.find())
    months = mongo.db.months.find().sort("_id", -1)

    if session["user"]:
        return render_template("my_expenses.html", username=username, expenses=expenses, months=months)
    
    return redirect(url_for("login"))


@app.route("/new_expense", methods=["GET", "POST"])
def new_expense():
    if request.method == "POST":
        new_expense = {
            "date": request.form.get("date"),
            "category_name": request.form.get("category_name"),
            "expense_description": request.form.get("expense_description"),
            "expense_amount": float(request.form.get("expense_amount")),
            "created_by": session["user"]
        }
        mongo.db.expenses.insert_one(new_expense)
        flash("Expense successfully added")
        return redirect(url_for("home_page"))
    
    expenses = mongo.db.expenses.find()
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("new_expense.html", categories=categories)


@app.route("/edit_expense/<expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    if request.method == "POST":
        updated_expense = {
            "date": request.form.get("date"),
            "category_name": request.form.get("category_name"),
            "expense_description": request.form.get("expense_description"),
            "expense_amount": float(request.form.get("expense_amount")),
            "created_by": session["user"]
        }
        mongo.db.expenses.update({"_id": ObjectId(expense_id)}, updated_expense)
        flash("Expense successfully updated")
    
    expense = mongo.db.expenses.find_one({"_id": ObjectId(expense_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_expense.html", expense=expense, categories=categories)


@app.route("/delete_expense/<expense_id>")
def delete_expense(expense_id):
    expenses = mongo.db.expenses.find()
    mongo.db.expenses.remove({"_id": ObjectId(expense_id)})
    flash("Expense deleted")
    return redirect(url_for("my_expenses", username=session["user"], expenses=expenses))


@app.route("/delete_account/<username>")
def delete_account(username):
    users = mongo.db.users.find()
    confirm_deletion = confirm(text="Are you sure you want to delete your account?\nThis can not be undone.", title="Confirm account deletion", buttons=["Yes, delete my account", "Cancel"])
    session.pop("user")
    mongo.db.users.remove({"username": username})
    flash("Your account was deleted. You will now be redirected to the home page.")
    return redirect(url_for("home_page", username=username, users=users))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), 
    port=int(os.environ.get("PORT")), 
    debug=True)