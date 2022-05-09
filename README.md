# AotYHelper
Capstone 2022 Submission For Fordham University Computer Science Masters Program


### Steps
1. Installation
2. Set enviromental variables
3. Initializing the application
4. Running the Dev Server
5. Create your admin account
6. Running Tests

## 1. Installation
```
git clone git@github.com:bengoodheart/capstone-final-submission.git
cd capstone-final-submission
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## 2. Enviromental Variables
There are several environmental variables you'll need to set off the bat for this to work.

AotYHelper leverages python-dotenv and os libraries to safetly obscure sensative information.

```
touch .env
nano .env
```
Paste the following and fill them in. 
```
DJANGO_SECRET_KEY=
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=
EMAIL_NAME=
EMAIL_PASS=
```
To generate a Django secret key go [here](https://django-secret-key-generator.netlify.app/)

For more information on generating the spotify credentials, go [here]("https://developer.spotify.com/documentation/general/guides/authorization/code-flow/)

For the email and pass, use your own so the backend can send emails for the password reset.

## 3. Initializing the Application

Double check you are in ```capstone-final-submission/``` and run the command:
```
python3 manage.py migrate
```

## 4. Run The Dev Server
Ensure your application will work by running the command:
```
python3 manage.py runserver
```

Then in your browser go to [localhost:8000](http://localhost:8000) and you should see the following:

![img](img.png)

Sweet! Now shut it down using `ctrl^C`

## 5. Create The Admin Account

Make sure in the root directory of the app `capstone-final-submission`

To use the website, you must create a user. You will want to create an admin user specifically.

```
python3 manage.py createsuperuser
```

Fill in the prompts, and make your account. 

Then go to http://127.0.0.1:8000/admin/  and log in

You can create, modify, and delete models.

## 6. Running Tests

With this application comes a test suite you use to get used to testing and examples of what kind of tests you can write. 

Additionally the application uses coverage.py, so you can see how much of the code is touched.

You can either runn the test suites once by using the command:
```
coverage run manage.py test
```

If you would like to test multiple times, use the runner app included by running 
```
python3 runner.py
``` 
and fill in the prompts.

To see the coverage report use:
```
coverage report
```
