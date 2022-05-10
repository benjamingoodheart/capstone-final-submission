# Django Depndencies
from django.contrib.auth.models import User
from django.db import IntegrityError

# models
from .models import Album, UserListenedTo, PlaysOn, Artist

# Custom Modules
from .utils import Utils

# Stdlib
import logging
import time
import os
import subprocess
import datetime
from urllib.parse import urlencode
import re
from dotenv import load_dotenv
import requests

# Middle Man For Handling Spotify requests
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
RESPONSE_CODE = os.getenv('RESPONSE_CODE')

# Index Constants for parsing the dates
YR_START = 0
YR_END = 4
MTH_START = 5
MTH_END = 7
DAY_START = 8
DAY_END = 10


class Spotify_Handler():
    def __init__(self, request) -> None:

        # Spotify Configuration
        load_dotenv()
        self.authorize_endpoint = 'https://accounts.spotify.com/authorize?'
        self.request = request
        self.scope = "user-read-recently-played"

        # 'Imports'
        self.u = Utils()

        # Logging Init
        logging.basicConfig(
                            filename="api.log",
                            format='%(asctime)s %(message)s',
                            filemode='a'
                            )
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    # Generate Authorize URL
    def genAuthURL(self) -> str():
        url = self.authorize_endpoint + "client_id=" + SPOTIFY_CLIENT_ID + \
            "&response_type=code" + "&redirect_uri=" + SPOTIFY_REDIRECT_URI + \
            "&scope=" + self.scope + "&show_dialog=true"
        return url

    def get_recently_played(self, headers):
        response = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=5", headers=headers)
        data = response.json()
        return data

    # Confirm the date is of the correct format
    def date_formatter(self, in_date) -> str():
        # First search for the full YYYY-MM-DD string
        date_str = re.findall(r'\d{4}-\d{2}-\d{2}', in_date)

        '''The nature of this function throws index errors a lot, but since we
        will always only need one date and the other variables are filled
        before the return statement, passing on theindex error should be OK'''

        try:
            year = date_str[0][YR_START:YR_END]
            month = date_str[0][MTH_START:MTH_END]
            day = date_str[0][DAY_START:DAY_END]
        except IndexError:
            pass

        if not date_str:
            day = "01"
            date_str = re.findall(r'\d{4}-\d{2}', in_date)
            try:
                year = date_str[0][YR_START:YR_END]
                month = date_str[0][MTH_START:MTH_END]
            except IndexError:
                pass

            if not date_str:
                month = "01"
                date_str = re.findall(r'\d{4}', in_date)
                year = date_str[0]
                if not date_str:
                    year = 1877  # Fun fact: this is the year of the earliest known recording!
                    return str(year) + "-" + str(month) + "-" + str(day)

        return str(year) + "-" + str(month) + "-" + str(day)

    # Iterate through the passed-in JSON catalogging the values
    def iterate_and_add_spotify_rec_played(self, request, data, headers) -> None:
        for i in data['items']:
            # ULT obj values
            album_name = i['track']['album']['name']
            album_art_url = i['track']['album']['images'][0]['url']
            raw_date = i['track']['album']['release_date']
            release_date = self.date_formatter(raw_date)

            # Get the album id and use that to pull other information about the album thats more easily sortable
            album_id = i['track']['album']['id']
            album_api_endpoint = "https://api.spotify.com/v1/albums/" + str(album_id)
            response = requests.get(album_api_endpoint, headers=headers)
            album_data = response.json()
            artist_name = album_data['artists'][0]['name']  # TODO: MORE THAN ONE ARTIST?
            label = album_data['label']
            user = request.user

            # Create the Object
            try:
                if self.u.user_already_listened(request, user, album_name, artist_name, release_date, label, album_art_url) is False:
                    self.u.createAlbum_FullOBJ(
                                        request, album_name, artist_name,
                                        release_date, label, album_art_url
                                        )
                    self.u.createUlt(user, album_name, artist_name)
            except IntegrityError:
                pass
