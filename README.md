# BUDGET HELPER

**BUDGET H£LP€R**

This constitutes the Data Centric Development Milestone Project.

https://budget-helper-project.herokuapp.com

## UX/Design

## Features

## Technologies Used

## Testing

## Deployment

To deploy the app to Heroku using Gitpod:

1. Install Flask via the Gitpod terminal with the command: 

    `pip3 install flask`

2. Import Flask in the app.py file:

    `from flask import Flask`

3. Install the Heroku toolbelt via the terminal with the command:

    `npm install -g heroku`

    Once installed, log in with your heroku login details using the command:

    `heroku login -i`

4. Redirect the list of dependencies used in the app to the requirements.txt file with the command:

    `pip3 freeze --local > requirements.txt`

5. Create the Procfile with the command:

    `echo web: python app.py > Procfile`

6. Log in to your Heroku account and select the app to be deployed. Click the 'Deploy' tab and select 'GitHub' as the deployment method.

7. Connect the GitHub account that has created this app's repository and search for the repository's name. Click 'Connect' once this is found.

8. Go to the Settings tab, scroll down and click on the 'Reveal Config Vars' button. Add the environment key-value pairs from the env.py file, ensuring to remove quotation marks when pasting them into Heroku.

9. After all Config Vars have been added, go back to the Gitpod terminal and add the requirements.txt and Procfiles:

    `git add requirements.txt Procfile`

    Commit these files and push the changes to Github.

10. The app is now ready to be deployed to Heroku. Go back to the Deploy tab, scroll down to the 'Automatic deploy' section and click 'Enable automatic deploys'. This updates the app on the Heroku platform each time changes are pushed to Github.

11. In the 'Manual deploy' section below, select the branch of the repository to be deployed. Once selected, click 'Deploy branch'.

12. The deployment may take a few minutes. Once complete, the message: "Your app was successfully deployed" will appear. Click on the 'View' button below the message to view the deployed app in a new browser tab and ensure everything is working as it should.

## Credits