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
    return render_template("index.html", expenses=expenses)


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


@app.route("/update_profile/<user_id>", methods=["GET", "POST"])
def update_profile(user_id):
    if request.method == "POST":
        updated_account = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email_address": request.form.get("email").lower(),
            "is_superuser": False
        }
        mongo.db.users.update({"_id": ObjectId(user_id)}, updated_account)
        flash("Your profile was successfully updated")
        return redirect(url_for("update_profile"))
    
    user = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
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
    
    if session["user"]:
        return render_template("profile.html", username=username)
    
    return redirect(url_for("login"))


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


@app.route("/delete_expense/<expense_id>")
def delete_expense(expense_id):
    expenses = mongo.db.expenses.find()
    mongo.db.expenses.remove({"_id": ObjectId(expense_id)})
    flash("Expense deleted")
    return redirect(url_for("my_expenses", username=session["user"], expenses=expenses))


@app.route("/delete_account/<user_id>")
def delete_account(user_id):
    users = mongo.db.users.find()
    session.pop("user")
    mongo.db.users.remove({"_id": ObjectId(user_id)})
    flash("Your account was deleted. You will now be redirected to the home page.")
    return redirect(url_for("home_page", username=session["user"], users=users))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), 
    port=int(os.environ.get("PORT")), 
    debug=True)