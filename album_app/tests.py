# Django Import
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.backends import ModelBackend
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.models import User

# Models and Forms
from .models import *
from .forms import *

# Std Lib
from datetime import datetime
import time
import string
import random
import logging
import uuid

# Progress Bar
from tqdm import tqdm

# Custom Modules
from .api import Spotify_Handler
from .utils import Utils

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager

# CONSTANT DECLARATION
UPPERCASE_CHARS = string.ascii_letters
TICKET_CHAR = UPPERCASE_CHARS + string.digits
ALL_CHARS = string.whitespace+string.ascii_letters + string.digits
STR_SIZE = 14
STR_SIZE_LABEL = 26


global gen_str
def gen_str(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))


TEST_TICKET_NUM = gen_str(STR_SIZE, TICKET_CHAR)

# Logger Declaration & Init
# from LOGGING.loggers in settings.py
logger = logging.getLogger(__name__)
logging.basicConfig(filename="test-results.log", format='%(asctime)s %(message)s', filemode='a')
logger.setLevel(logging.DEBUG)

logger.debug("\n")
logger.debug("\n")
logger.debug("TEST TICKET #:" + TEST_TICKET_NUM)
logger.debug("^^^^^^^^^^^^^^^^^^")
logger.debug("**********************")
logger.debug("**********************")
logger.debug("^^^^^^^^^^^^^^^^^^")
logger.debug("")

# To create Test User
global create_user
def create_user(name, password):
    return User.objects.create(username=name, password=password)


# Tests
# Tests the HTTP Response status of the pages
class StaticStatusTestCase(TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Static Status Test Case at " + str(converted))

    def setUp(self):
        self.c = Client()
        self.start_time = time.time()

    def testIndex(self):
        response = self.c.get('/', secure=True)
        self.assertEqual(response.status_code, 200)

    def testSettings(self):
        response = self.c.get('/settings', secure=True)
        self.assertEqual(response.status_code, 302)  # Login required, should redirect

    def testLoginPage(self):
        response = self.c.get('/accounts/login/', secure=True)
        self.assertEqual(response.status_code, 200)

    def testFeedBackStatus(self):
        response = self.c.get('/feedback', secure=True)
        self.assertEqual(response.status_code, 302)

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(end_time))
    run_time = (end_time - start_time) * 1000
    logger.debug("Ended Context Tests at: " + str(converted))
    logger.debug("Total time elapsed testing Static Status  " + str(run_time))


# Test the variables passed
class ContextTestCase(TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Context Test Case at " + str(converted))

    def setUp(self):
        self.c = Client()

    def testIndex(self):
        now = time.time()
        response = self.c.get('/', secure=True)
        exp_answer = "<h4>Please register</h4>"
        response = response.context['register']
        self.assertEqual(response, exp_answer)

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(end_time))
    run_time = (end_time - start_time) * 1000
    logger.debug("Ended Context Tests at: " + str(converted))
    logger.debug("Total time elapsed testing Context Tests  " + str(run_time))


# Test the content returned in the response
class SiteContentTestCase(TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Content Test Case at " + str(converted))

    def setUp(self):
        self.c = Client()
        self.user = create_user('aotybot', 'password')
        self.c.login(username="aotybot", password="password")

    def testIndexContent(self):
        response = self.c.get("/", secure=True)
        content = response.content
        self.assertContains(response, "We help ya rank ya albums")

    def testSettingsContent(self):
        self.c.force_login(user=self.user)
        response = self.c.get('/settings', secure=True)
        self.assertContains(response, "Coming Soon")

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    run_time = end_time - start_time
    logger.debug("Ended Content Tests at: " + str(converted))
    logger.debug("Total time elapsed testing Content Tests  " + str(run_time))


# Tests the album object
class albumObjectTestCase(TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Album Obj Test Case at " + str(converted))

    @classmethod
    def setUpTestData(cls):
        cls.c = Client
        cls.u = Utils()
        cls.album = Album.objects.create(albumName="RandomName", release_date="2022-01-01")
        cls.factory = RequestFactory()

    def gen_string(self, str_size, allowed_chars):
        return ''.join(random.choice(allowed_chars) for x in range(str_size))

    def testBadDate(self):
        bad_date = "111122"
        try:
            self.album.release_date = bad_date
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def testGoodDate(self):
        good_date = "2022-01-11"
        try:
            self.album.release_date = good_date
        except:
            self.assertTrue(False)

    def testRandName(self):
        chars = string.ascii_letters + string.punctuation
        name = self.gen_string(12, chars)
        try:
            self.album.albumName = name
        except:
            self.assertTrue(False)

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(end_time))
    run_time = (end_time - start_time)
    logger.debug("Ended Album Obj Test Case at at: " + str(converted))  # Unix to time converter
    logger.debug("Total time elapsed testing Album Obj  " + str(run_time))


class AuthenticationTestCase(TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Auth Test Case at " + str(converted))

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='aotyhelperbot@gmail.com', password='password!')

    def testloginSuccessful(self):
        test_login = self.c.login(username='aotyhelperbot@gmail.com', password='password!')
        self.assertTrue(test_login)
        self.c.get("/")

    def testSettingsPermission(self):
        test_login = self.c.force_login(user=self.user)
        response = self.c.get('/settings', secure=True)
        web = "Apple Music"
        self.assertContains(response, web)

    def testCreatePermission(self):
        test_login = self.c.login(username='aotyhelperbot@gmail.com', password='password!')
        response = self.c.get('/add_album', secure=True)
        web = "Add a new record"
        self.assertContains(response, web)

    # Try x amount of randomly generated strings to brute force log in
    def testmadAttempts(self):
        sub_start = time.time()
        converted = datetime.fromtimestamp(int(sub_start))
        logger.debug("Started mad attempts at: " + str(converted))
        for _ in range(1, 100):
            username = gen_str(STR_SIZE, ALL_CHARS)
            password = gen_str(STR_SIZE, ALL_CHARS)
            test_login = self.c.login(username=username, password=password)
            self.assertFalse(test_login)

        sub_end = time.time()
        converted = datetime.fromtimestamp(int(sub_end))
        runtime = sub_end - sub_start
        logger.debug('Ended mad attempts at: ' + str(converted))
        logger.debug('Runtime for mad attempts: ' + str(runtime))

    def testSettingsPermissionDenied(self):
        response = self.c.get('/settings', secure=True)
        self.assertEqual(response.status_code, 302)

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(end_time))
    run_time = end_time - start_time
    logger.debug("Ended Auth Tests at: " + str(converted))
    logger.debug("Total time elapsed testing Auth  " + str(run_time))


class ModelTestCase(TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Model Test Case at " + str(converted))

    def setUp(self):
        self.user = create_user('aotyhelperbot', 'password')
        self.f = RequestFactory()
        self.request = self.f.request()

        self.artist_name = gen_str(STR_SIZE, ALL_CHARS)
        self.album_name = gen_str(STR_SIZE, ALL_CHARS)
        self.label_name = gen_str(STR_SIZE, ALL_CHARS)

        self.artist_obj = Artist.objects.create(artistName=self.artist_name)
        self.album_obj = Album.objects.create(albumName=self.album_name)
        self.playsOn_obj = PlaysOn.objects.create(FK_albumID_PlaysOn=self.album_obj, FK_artistID=self.artist_obj)
        self.label = RecordLabel.objects.create(recordLabelName=self.label_name)

    def testArtistdisplayStr(self):
        display_str = self.artist_obj.__str__()
        exp = self.artist_name
        self.assertEqual(display_str, exp)

    def testPlaysOnDefaultDisplayStr(self):
        display_str = self.playsOn_obj.__str__()
        exp_str = "Artist plays On Album"
        self.assertEqual(display_str, exp_str)

    def testPlaysOnCustom(self):
        self.playsOn_obj.display_artist_name = self.artist_name
        self.playsOn_obj.display_album_name = self.album_name
        self.playsOn_obj.save()
        display_str = self.playsOn_obj.__str__()
        exp_str = str(self.artist_name) + " plays On " + str(self.album_name)

    def testUltAbsURL(self):
        user = self.user
        request = self.request
        album_name = self.album_name
        artist_name = self.artist_name
        release_date = "2042-10-31"
        record_label = gen_str(STR_SIZE, ALL_CHARS)
        img_url = "https://www.aotyhelper.net"
        ult_obj = UserListenedTo.objects.create(user=user, FK_albumID_userLT=self.album_obj, FK_artistID=self.artist_obj, FK_release_date_LT=release_date, FK_recordLabelID_LT=self.label)
        abs_url = ult_obj.get_absolute_url()
        exp_res = reverse('detailView', args=[str(ult_obj.ultID)])
        self.assertEquals(abs_url, exp_res)

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(end_time))
    run_time = end_time - start_time
    logger.debug("Ended Form Tests at: " + str(converted))
    logger.debug("Total time elapsed testing Models  " + str(run_time))


class FormTestCase(TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Form Test Case at " + str(converted))

    def setUp(self):
        self.user = create_user('user', "!drowssap")

    def testValidForm(self):
        feedback = Feedback.objects.create(feedback_text='blahblahba', made_by_id=self.user.id)
        data = {'feedback_form': feedback.feedback_text}
        form = FeedbackForm(data=data)
        self.assertTrue(form.is_valid)

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(end_time))
    run_time = end_time - start_time
    logger.debug("Ended Form Tests at: " + str(converted))
    logger.debug("Total time elapsed testing Forms  " + str(run_time))


class apiModuleTestCase(TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started API Test Case at " + str(converted))

    def setUp(self):
        self.f = RequestFactory()
        self.request = f.request()

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(end_time))
    run_time = end_time - start_time
    logger.debug("Ended API Tests at: " + str(converted))
    logger.debug("Total time elapsed testing API  " + str(run_time))


class viewsTestCase(TestCase):

    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Views Test Case at " + str(converted))

    def setUp(self):
        self.c = Client()
        self.user = create_user('aotyhelper', 'password!')
        self.c.login(username='aotyhelper', password='password!')

    def testIndexView(self):
        self.c.login(username='aotyhelper', password='password!')
        response = self.c.get('indexView', secure=True)
        self.assertEqual(response.status_code, 302)

    def testsettingsView(self):
        response = self.c.get('settingsView', secure=True)
        self.assertEqual(response.status_code, 302)

    def testcallback(self):
        response = self.c.get('callback', secure=True)
        self.assertEqual(response.status_code, 302)

    def feedbackView(self):
        response = self.c.get('feedbackView', secure=True)
        self.assertEqual(response.status_code, 200)

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(end_time))
    run_time = end_time - start_time
    logger.debug("Ended Views Tests at: " + str(converted))
    logger.debug("Total time elapsed testing Views  " + str(converted))


class utilsTestCase(TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Utils Test Case at " + str(converted))

    def setUp(self):
        self.u = Utils()

        self.album_name = gen_str(STR_SIZE_LABEL, ALL_CHARS)
        self.artist_name = gen_str(STR_SIZE_LABEL, ALL_CHARS)
        self.user = User()
        self.f = RequestFactory()
        self.request = self.f.request()
        album_obj = Album.objects.create(albumName=self.album_name)
        artist_obj = Artist.objects.create(artistName=self.artist_name)
        self.label_name = gen_str(STR_SIZE_LABEL, ALL_CHARS)
        self.label = RecordLabel.objects.create(recordLabelName=self.label_name)
        self.playedOn = PlaysOn.objects.create(FK_artistID=artist_obj, display_artist_name=self.artist_name, FK_albumID_PlaysOn=album_obj, display_album_name=self.album_name,)

    def testAlbumExists(self):
        test = self.u.album_exists(self.album_name)
        self.assertTrue(test)

    def testAlbumDoesNotExist(self):
        badName = gen_str(STR_SIZE, ALL_CHARS)
        test = self.u.album_exists(badName)
        self.assertFalse(test)

    def testLabelExists(self):
        test = self.u.labelExists(self.label_name)
        self.assertTrue(test)

    def testArtistExists(self):
        artist_name = gen_str(STR_SIZE, ALL_CHARS)
        self.u.artist_exists(artist_name)

    def testGetBC_Username(self):
        get_bc = self.u.getBC_Username()
        self.assertEqual(type("test"), type(get_bc))

    def testCreateAlbum_FullOBJ(self):
        request = self.request
        album_name = self.album_name
        artist_name = self.artist_name
        release_date = "2042-10-31"
        record_label = self.label
        img_url = "https://www.aotyhelper.net"
        tags = ['punk', 'dub', 'rap']

        self.u.createAlbum_FullOBJ(
                                request, album_name, artist_name,
                                release_date, record_label, img_url,
                                tags[0], tags[1], tags[2]
                                )

    def testplaysOn_exists(self):
        test = self.u.playsOn_exists(album_name=self.album_name, artist_name=self.artist_name)
        self.assertTrue(test)

    # END LOG
    end_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    run_time = end_time - start_time
    logger.debug("Ended Utils Tests at: " + str(converted))
    logger.debug("Total time elapsed testing Utils  " + str(run_time))


class UserProfileTestSuite(TestCase):
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Utils Test Case at " + str(converted))

    def setUp(self):
        self.user = create_user('aotyhelperbot', 'password')
        self.f = RequestFactory()
        self.request = self.f.request()
        self.c = Client()

    def testUserProfileTokens(self):
        access_token = gen_str(STR_SIZE, ALL_CHARS)
        refresh_token = gen_str(STR_SIZE, ALL_CHARS)
        self.user.profile.spotifyAccessToken = access_token
        self.user.profile.spotifyRefreshToken = refresh_token
        self.user.profile.save()

        self.assertEqual(access_token, self.user.profile.spotifyAccessToken)
        self.assertEqual(refresh_token, self.user.profile.spotifyRefreshToken)

    def testUserLogOutTokens(self):
        access_token = gen_str(STR_SIZE, ALL_CHARS)
        refresh_token = gen_str(STR_SIZE, ALL_CHARS)

        self.c.login(user='aotyhelperbot', password='password')
        self.user.profile.spotifyAccessToken = access_token
        self.user.profile.spotifyRefreshToken = refresh_token
        self.user.profile.save()

        self.c.logout()
        self.c.login(user='aotyhelperbot', password='password')

        self.assertEqual(access_token, self.user.profile.spotifyAccessToken)
        self.assertEqual(refresh_token, self.user.profile.spotifyRefreshToken)

    end_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    run_time = end_time - start_time
    logger.debug("Ended UserProfile Tests at: " + str(converted))
    logger.debug("Total time elapsed testing UserProfile  " + str(run_time))
