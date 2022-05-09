from platform import release
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import time
from datetime import datetime
import json
import re
import logging


class Scraper():
    def __init__(self, bc_username) -> None:
        self.bc_username = bc_username
        self.main_driver = (self.newDriver())
        self.i = 1
        self.pre_json = {
            self.i: {
                'album_name': '',
                'artist_name': '',
                'month': '',
                'day': '',
                'year': '',
                'record_label': '',
                'image_url': ''
            }}

        # logging init
        logging.basicConfig(
                            filename="api.log",
                            format='%(asctime)s %(message)s',
                            filemode='a'
                            )
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def __del__(self):
        self.parentDriverTearDown()

    # Firefox needs the geckodriver to operate. It operates on headless since
    # it's operating from the command line of a display-less server.abs
    def newDriver(self) -> webdriver:
        firefoxOptions = Options()
        firefoxOptions.add_argument("--headless")
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefoxOptions)
        return driver

    def parentDriverTearDown(self) -> None:
        session_id = str(self.main_driver.session_id)
        self.main_driver.close()

    def childDriverTearDown(self, driver) -> None:
        driver.close()

    def openUserPage(self) -> None:
        self.main_driver.get("https://bandcamp.com/" + self.bc_username)

    def collectionCount(self) -> int:
        collection_count = self.main_driver.find_element(By.XPATH, ("/html/body/div[7]/div/div[1]/div[1]/div[2]/div[1]/div/ol/li[1]/span/span"))
        count = int(collection_count.text)
        return count

    # To load more albums on the bandcamp page
    def loadMore(self):
        time.sleep(1)
        load_more = self.main_driver.find_element_by_xpath("/html/body/div[7]/div/div[1]/div[1]/div[2]/div[2]/div/div/div/button")
        time.sleep(1)
        load_more.click()

        html = self.main_driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)

    # Iterate through the links on the bandcamp page
    def getLinks(self, num_albums):
        album_links = self.main_driver.find_elements(By.XPATH, "/html/body/div[7]/div/div[1]/div[1]/div[2]/div[2]/div/div/ol")
        links = self.main_driver.find_elements(By.CLASS_NAME, 'item-link')
        for x in links[0:num_albums]:
            url = x.get_attribute('href')
            print(url)
            if url is not None:
                # New Driver Opens Up
                art_driver = self.newDriver()
                art_driver.get(url)
                self.assignToVar(art_driver)

                self.childDriverTearDown(art_driver)
            else:
                pass

    # Assign the scraped values to variabels
    def assignToVar(self, driver):
        album_name = driver.find_element(By.CLASS_NAME, "trackTitle").text
        print(album_name)
        artist_name = driver.find_element(By.TAG_NAME, 'h3').text
        release_date = driver.find_element(By.XPATH, "//*[contains(text(), 'released')]").text
        image_url = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[1]/div[2]/div[2]/div[1]/a/img")
        # TODO: URL VALIDATION????
        parsedDate = self.parseDate(release_date)
        parsedName = self.parseArtist(artist_name)
        record_label = self.findRecordLabel()

        self.createJSON(album_name, parsedName, parsedDate, record_label, image_url)

    def parseDate(self, date_string) -> list:
        month = re.findall(r"\s(January|February|March|April|May|June|July|August|September|October|November|December)\s", date_string)[0]
        day = re.findall(r"[\d]{1,2}", date_string)[0]
        year = re.findall(r"[\d]{4}", date_string)[0]
        parsedDate = [month, day, year]
        return parsedDate

    def parseArtist(self, artist_string) -> str:
        just_artist_name = artist_string.strip("by ")
        return just_artist_name

    def findRecordLabel(self) -> str:
        # scrape for record label in google or itunes backend?
        # for now:
        record_label = 'Placeholder Records'
        return record_label

    def createJSON(self, album_name, artist_name, release_date, record_label, image_url) -> None:
        self.pre_json[self.i]["album_name"] = album_name
        self.pre_json[self.i]["artist_name"] = artist_name
        self.pre_json[self.i]["month"] = release_date[0]
        self.pre_json[self.i]["day"] = release_date[1]
        self.pre_json[self.i]["year"] = release_date[2]
        self.pre_json[self.i]['record_label'] = record_label
        self.pre_json[self.i]['image_url'] = image_url

        self.i += 1
        self.pre_json[self.i] = {}

        print(self.getJSON())

    def exportJSON(self) -> None:
        json_object = json.dumps(self.pre_json, indent=4)
        with open("../bandcamp_collection.json", 'a') as outfile:
            outfile.write(json_object)
            outfile.write(", \n")
            outfile.close()

    def getJSON(self):
        return self.pre_json
