# Django Dependencies
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist

# Custom Modules
from .utils import *
from .api import Spotify_Handler

# Stdlib
from datetime import datetime
import logging
import time
import uuid
import os
import secrets
import string
import datetime
from datetime import date
import json
from urllib.parse import urlencode
import sys

# Imported Modules
from dotenv import load_dotenv
import requests

# forms
from .forms import *

# models
from .models import RecordLabel, Album, Genre, AlbumArt

# global variables
load_dotenv()

# Logging set up
logger = logging.getLogger('app_api')  # from LOGGING.loggers in settings.py
logging.basicConfig(filename="views.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Constant Declaration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
RESPONSE_CODE = os.getenv('RESPONSE_CODE')
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
ME_URL = 'https://api.spotify.com/v1/me'
RECENTLY_PLAYED_URL = 'https://api.spotify.com/v1/me/player/recently-played?limit=50'

CURRENT_DATE_TIME = datetime.datetime.now()
CURR_DATE = CURRENT_DATE_TIME.date()
CURR_YEAR = CURR_DATE.strftime('%Y')


# VIEWS
'''Views pass information through context dictionary objects. When you see
context['some_item'], variable is being maniuplated on the front end side'''


# Landing page aka list view in CRUD parlance
def index(request):
    context = {}

    # Have to pass in the request as Spotify_Handler needs to use the user info
    s = Spotify_Handler(request)

    if not request.user.is_authenticated:
        # If the user is not logged in, they will see the please register message
        context['register'] = "<h4>Please register</h4>"
    else:

        user = request.user

        # Restore the Spotify Access and Refresh Tokens for persistance
        # between sessions
        request.session['tokens'] = {
                                    'access_token': user.profile.spotifyAccessToken,
                                    'refresh_token': user.profile.spotifyRefreshToken
                                }

        if user.profile.hasSpotify is True:
            context['spotify'] = True
        else:
            context['spotify'] = False

        '''Collect a list of years from the albums the
        user has listened to to build a drop down list '''
        years_list = UserListenedTo.objects.filter(user=request.user)
        unique_years = set()
        for years in years_list:
            if years.FK_release_date_LT.year not in unique_years:
                unique_years.add(years.FK_release_date_LT.year)
            else:
                pass

        context['unique_years'] = unique_years
        context['CURR_YEAR'] = CURR_YEAR
        context['all_albums'] = UserListenedTo.objects.filter(user=request.user, FK_release_date_LT__startswith=CURR_YEAR)

    context['today'] = date.today()
    return render(request, 'index.html', context)


# Manual create view for a UserListenedTo Object
# TODO: TEST This function
@login_required
def createView_album(request):
    u = Utils()
    context = {}
    context['today'] = date.today()

    # Initialize Entity Forms
    albumInput = AlbumForm(request.POST or None)
    artistInput = ArtistForm(request.POST or None)
    imageUrlInput = ImageURLForm(request.POST or None)
    recordLabelInput = RecordLabelForm(request.POST or None)

    # Init Relationship Forms
    playsOnInput = PlaysOnForm(request.POST or None)
    releasedInput = ReleasedForm(request.POST or None)
    

    # Object from Form creation
    forms_validated = set({})   # set to be used for conditionals

    if albumInput.is_valid():
        album_obj = albumInput.save()
        forms_validated.add(albumInput)
    if artistInput.is_valid():
        artist_obj = artistInput.save()
        forms_validated.add(artistInput)
    if imageUrlInput.is_valid():
        imageURL_obj = imageUrlInput.save()
        AlbumArt.objects.create(
                                urlID=imageURL_obj,
                                display_album_name=album_obj.albumName
        )
        forms_validated.add(imageUrlInput)

    # Object from form input creation: Record Label
    if releasedInput.is_valid():
        released_obj = releasedInput.save()
        rln = str(released_obj.display_recordLabelName)
        u.labelExists(rln)  # Validate whether the label exists and if it doesnt it creates it and keeps goin on
        released_obj.FK_albumID_Released = Album.objects.get(albumID=album_obj.albumID)
        released_obj.display_album_name = str(Album.objects.get(albumName=album_obj.albumName))
        released_obj.FK_recordLabelID = RecordLabel.objects.get(recordLabelName=released_obj.display_recordLabelName)
        released_obj.save()
        forms_validated.add(releasedInput)

    # If all the pertinent parts of the form are created, create the ULT object
    if albumInput and artistInput and imageUrlInput and releasedInput in forms_validated:
        u.createAlbum_FullOBJ(request, album_obj.albumName, artist_obj.artistName, album_obj.release_date, released_obj.display_recordLabelName, imageURL_obj.url)
        user = request.user
        u.createUlt(user, album_obj.albumName, artist_obj.artistName)
        return redirect("/")

    context['albumInput'] = albumInput
    context['artistInput'] = artistInput
    context['imageUrlInput'] = imageUrlInput
    context['releasedInput'] = releasedInput

    return render(request, "create_view_album.html", context)


# Detail View - Where the editable album pages are rendered
@login_required
def detailView(request, ultID):
    context = {}

    ult_obj = UserListenedTo.objects.get(ultID=ultID)
    albumart_obj = AlbumArt.objects.get(display_album_name=ult_obj.FK_albumID_userLT)

    context['data'] = ult_obj
    context['album'] = albumart_obj
    context['today'] = date.today()

    return render(request, 'detail_view.html', context)


# User can update comments and ratings
@login_required
def editView(request, ultID):
    context = {}

    ult_obj = UserListenedTo.objects.get(ultID=ultID)
    albumart_obj = AlbumArt.objects.get(display_album_name=ult_obj.FK_albumID_userLT)
    ulf = UserListenedToForm(request.POST or None, instance=ult_obj)

    if ulf.is_valid():
        ulf.save()
        return redirect('detailView', ult_obj.ultID)

    context['data'] = ult_obj
    context['album'] = albumart_obj
    context['ulf'] = ulf
    context['today'] = date.today()

    return render(request, "edit_view.html", context)


# A user can choose to delete albums from their collection
@login_required
def deleteView(request, ultID):
    context = {}
    ult_obj = UserListenedTo(ultID=ultID, user=request.user)

    if request.method == "POST":
        ult_obj.delete()
        return HttpResponseRedirect("/")

    context['data'] = ult_obj
    context['today'] = date.today()

    return render(request, "delete_view.html", context)


# Settings Page
@login_required(login_url="/accounts/login")
def settingsView(request):
    context = {}
    user = request.user

    # Authorization Flow For Spotify
    state = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
    )

    if request.session.get('loginout') is None:
        request.session['loginout'] = 'logout'

    # Refer to https://developer.spotify.com/documentation/general/guides/authorization/scopes/ for list of scopes
    scope = 'user-read-recently-played'

    loginout = request.session['loginout']

    # See if Spotify needs to open the authorization portal
    if loginout == 'logout':
        payload = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'state': state,
            'scope': scope,
            'show_dialog': True,
        }
    elif loginout == 'login':
        payload = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'state': state,
            'scope': scope,
        }
    else:
        raise Http404

    # Build the search query for the API link
    qs = '?' + urlencode(payload)
    url = AUTH_URL + qs
    url = str(url)

    # Set the auth state
    request.session['spotify_auth_state'] = state

    context['spotify_con'] = user.profile.hasSpotify
    context['auth_url'] = url
    context['payload'] = payload
    context['loginout'] = request.session['loginout']
    context['today'] = date.today()

    return render(request, "settings.html", context)


# The landing confirmation page for once the Spotify Authorization is complete
@login_required
def callbackView(request):
    context = {}
    user = request.user
    state = request.GET.get('state')
    code = request.GET.get('code')
    stored_state = request.session['spotify_auth_state']

    if state is None or state != stored_state:
        logger.error('Error message: State mismatch')

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI
    }

    response = requests.post(
                            TOKEN_URL, auth=(
                                            SPOTIFY_CLIENT_ID,
                                            SPOTIFY_CLIENT_SECRET
                                            ),
                            data=payload)
    response_data = response.json()

    if response_data.get('error') or response.status_code != 200:
        logger.error('Failed to recieve token: %s', response_data.get('error'))

    # Set the tokens in the session
    request.session['tokens'] = {
                                'access_token': response_data.get('access_token'),
                                'refresh_token': response_data.get('refresh_token')
                                }

    request.session['loginout'] = 'login'

    # Set tokens for session persistance
    user.profile.spotifyAccessToken = request.session.get('tokens').get('access_token')
    user.profile.spotifyRefreshToken = request.session.get('tokens').get('refresh_token')
    user.profile.hasSpotify = True
    user.profile.save()

    context['cookies'] = request.session.get('loginout')
    context['state'] = response_data
    context['success'] = "Success! Your Spotify is connected"
    context['today'] = date.today()

    return render(request, "settings.html", context)


# To retrieve a refreshed token
@login_required
def refreshTokenView(request):

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': request.session['tokens']['refresh_token']
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(
                            TOKEN_URL, auth=(
                                            SPOTIFY_CLIENT_ID,
                                            SPOTIFY_CLIENT_SECRET
                                            ),
                            data=payload, headers=headers
                            )
    response_data = response.json()

    request.session['tokens']['access_token'] = response_data['access_token']

    return redirect('/')


# The funciton that retrieves the new spotify data
@login_required
def getNewFromSpotifyView(request):
    user = request.user
    if user.profile.hasSpotify is False:
        context['sorry'] = 'This only works for spotify users at the moment!'
    else:
        context = {}
        s = Spotify_Handler(request)
        headers = {'Authorization': f"Bearer {request.session['tokens']['access_token']}"}

        response = requests.get(RECENTLY_PLAYED_URL, headers=headers)
        response_data = response.json()

        # Add the albums to the database
        
        s.iterate_and_add_spotify_rec_played(request, response_data, headers)

        # Context Return
        context['response'] = response.status_code
        context['json'] = response_data
        context['today'] = date.today()

    return render(request, 'spotify.html', context)


# A feedback form for user feedback
@login_required
def feedbackView(request):
    context = {}
    context['today'] = date.today()

    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        # build the Email
        # Currently this gets stored on the server

        if feedback_form.is_valid():
            subject = "NEW FEEDBACK: " + feedback_form.cleaned_data['category']
            from_email = 'aotybot@aotyhelper.net'
            pre_text = feedback_form.cleaned_data['feedback_text']
            logger.debug(type(subject))

            sig = "\n\n\n==============\nFeedback submitted by: " + \
                str(request.user) + " ||\n==============\n\n\n"

            message = str(pre_text + sig)
            logger.debug("Post-processed-text: " + message)
            logger.debug(type(message))
            try:
                send_mail(str(subject), str(message), from_email, ['bgoodheart@fordham.edu'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackForm()
        context['feedback_form'] = feedback_form

    return render(request, "feedback.html", context)


# Error Messages
def view_404(request, exception=None):
    # TODO - ADD TOASTS
    return redirect('/')


def view_500(request, exception=None):
    return redirect('/')
