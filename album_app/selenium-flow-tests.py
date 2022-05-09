# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import unittest
import time
import os
from dotenv import load_dotenv
import random
import string
import logging
from datetime import datetime

# CONSTANT DECLARATION
MAX_LIMIT = 255
UPPERCASE_CHARS = string.ascii_letters
TICKET_CHAR = UPPERCASE_CHARS + string.digits 
STR_SIZE = 14

global gen_str
def gen_str(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))
TEST_TICKET_NUM = gen_str(STR_SIZE, TICKET_CHAR)

# Logger Declaration & Init
# from LOGGING.loggers in settings.py
logger = logging.getLogger(__name__)
logging.basicConfig(filename="test-results.log", format='%(asctime)s %(message)s', filemode='a')
logger.setLevel(logging.DEBUG)

logger.debug("SELENIUM TEST TICKET #:" + TEST_TICKET_NUM)

logger.debug("**********************")
logger.debug("SELENIUM TEST TICKET #:" + TEST_TICKET_NUM)
logger.debug("**********************")



class fullFlowTestCase(unittest.TestCase):
    # START LOG
    start_time = time.time()
    converted = datetime.fromtimestamp(int(start_time))
    logger.debug("Started Full Flow Test Case at "+ str(converted))
    
    def setUp(self):
        firefoxOptions = Options()
        firefoxOptions.add_argument("--headless")
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefoxOptions)
        load_dotenv()
        self.driver.get("https://aotyhelper.net")

    def randStrGen(self) -> str():
        random_string = ''
        for i in range(12):
            random_integer = random.randint(0, MAX_LIMIT)
            random_string += chr(random_integer)

        return random_string

    def tearDown(self):
        self.driver.quit()

    def testFullFlow(self):
        user = os.getenv('TEST_USER')
        pw = os.getenv('TEST_PASS')
        spot_name = os.getenv('SPOT_NAME')
        spot_pass = os.getenv('SPOT_PASS')

        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "id_username").send_keys(user)
        self.driver.find_element(By.ID, "id_password").send_keys(pw)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/div/div[3]/div/form/input[2]").click()
        time.sleep(1)

        # Go to Settings
        self.driver.find_element(By.LINK_TEXT, "Settings").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Connect Your Spotify!").click()
        time.sleep(1)

        # Log into spotify
        self.driver.find_element(By.ID, "login-username").send_keys(spot_name)
        self.driver.find_element(By.ID, "login-password").send_keys(spot_pass)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[2]/div[3]/div[2]/button/div[1]").click()
        time.sleep(3)

        # Authorize access
        self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div/div[3]/button/div[1]").click()
        time.sleep(1)

        # Go back Home, now authorized
        self.driver.find_element(By.LINK_TEXT, "Home").click()
        time.sleep(1)

        # Refresh The Listens
        self.driver.get("https://aotyhelper.net/get_new/spotify")
        time.sleep(1)

        # Go back Home, now authorized
        self.driver.find_element(By.LINK_TEXT, "Home").click()
        time.sleep(1)

        # Log Out
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(1)

    def testAlbumDetailsFlow(self):
        user = os.getenv('TEST_USER')
        pw = os.getenv('TEST_PASS')

        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "id_username").send_keys(user)
        
        self.driver.find_element(By.ID, "id_password").send_keys(pw)
        self.driver.find_element(By.XPATH, "/html/body/div/div[3]/div/form/input[2]").click()

        self.driver.find_element(By.LINK_TEXT, "Everything Was Beautiful").click()
        self.driver.find_element(By.CLASS_NAME, "z-depth-3")
        time.sleep(1)

    def testEditAlbum(self):
        user = os.getenv('TEST_USER')
        pw = os.getenv('TEST_PASS')

        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "id_username").send_keys(user)
        self.driver.find_element(By.ID, "id_password").send_keys(pw)
        self.driver.find_element(By.XPATH, "/html/body/div/div[3]/div/form/input[2]").click()

        self.driver.find_element(By.LINK_TEXT, "Everything Was Beautiful").click()
        self.driver.find_element(By.CLASS_NAME, "z-depth-3")
        self.driver.find_element(By.LINK_TEXT, "Edit").click()

        comment = self.driver.find_element(By.ID, "id_comment")
        comment.send_keys(self.randStrGen())

        self.driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[3]/div[2]/div[2]/form/input[2]"
                                ).click()
    # END LOG
    # NO END LOG
    
if __name__ == '__main__':
    unittest.main()
