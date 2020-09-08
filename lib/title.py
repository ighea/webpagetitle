import logging, sys, os, lxml
import requests

if os.environ.get('FLASK_ENV') != "production":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from requests_html import HTMLSession

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

class NoTitleError(Exception):
    pass

class Title:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.method = None

    # Fetch url with fallback support
    def fetch(self, timeout = 10):
        try:
            return self.fetch_selenium(timeout)
        except (NoTitleError, WebDriverException):
            try:
                return self.fetch_requests(timeout)
            except requests.exceptions.ConnectionError:
                return False

    def fetch_requests(self, timeout):
        logging.debug("Fetching with requests...")

        self.method = "requests"
        response = HTMLSession().get(self.url, timeout = timeout)
        if(response.status_code != 200):
            return False
        try:
            title = response.html.find('title', first=True).text
        except:
            return False
        self.title = title

        return True

    def fetch_selenium(self, timeout):
        logging.debug("Fetching with selenium...")

        self.method = "selenium"

        options = Options()
        options.headless = True
        #options.log.level = "trace" # For debugging issues with firefox and geckodriver

        firefox_profile = FirefoxProfile()
        # Disable CSS
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        # Disable images
        firefox_profile.set_preference('permissions.default.image', 2)
        # Disable Flash
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        browser = webdriver.Firefox(capabilities=DesiredCapabilities().FIREFOX, options=options, firefox_profile=firefox_profile)
        browser.set_page_load_timeout(timeout)
        browser.get(self.url)
        title = browser.title
        source = browser.page_source
        logging.debug("SOURCE: " + source)
        browser.quit()

        logging.debug("Selenium retrieved title: " + title)

        self.title = title

        if len(title) == 0:
            raise NoTitleError("Selenium no title.")

        return True

    # get title for page
    def get_title(self):
        return self.title

    # return method name used for title retrieval ("selenium" or "requests")
    def get_method(self):
        return self.method
