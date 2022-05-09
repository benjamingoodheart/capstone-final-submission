# AotYHelper
Capstone 2022 Submission For Fordham University Computer Science Masters Program


### Steps
1. Installation
2. Set enviromental variables
3. Running the Dev Server
4. Running Tests

## 1. Installation
```
git clone git@github.com:bengoodheart/capstone-final-submission.git
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

