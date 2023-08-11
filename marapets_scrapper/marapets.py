import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from .actions import login
from .objects import Scraper

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

logging.basicConfig()


class Marapets(Scraper):
    def __init__(self):
        self.base_url = "https://www.marapets.com/"
        self.driver = self.initialize()
        login(driver=self.driver)
