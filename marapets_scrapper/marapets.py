import logging

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .actions import login
from .objects import Scraper

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

logging.basicConfig()


class Marapets(Scraper):
    def __init__(self):
        self.base_url = "https://www.marapets.com/"
        self.driver = self.initialize()
        login(driver=self.driver)

    def automate(self):
        self.driver.get("https://www.marapets.com/quest_games.php")
        dives_data = self.get_elements_by_time(
            by=By.XPATH,
            value="//div[@class='gamespage_eachbox hideforchanges']",
            single=False,
        )
        dives = [
            self.get_elements_by_time(
                by=By.XPATH, value=".//a[contains(@href,'marapets')]", base=item
            )
            for item in dives_data
            if item
        ]
        titles = [
            self.get_elements_by_time(
                by=By.XPATH, value='.//div[@class="gamespage_eachbox_title"]', base=item
            )
            for item in dives_data
            if item
        ]

        dives = [item.get_attribute("href") for item in dives if item]
        titles = [item.text for item in titles if item]
        num = 0
        for num, title in zip(range(len(titles)), titles):
            print(f"{num}: {title}")
        num = num + 1
        print(f"{num}: solve all quest")
        while True:
            choice = int(input("\n\n\nPlease Enter Choice: "))
            if choice <= num:
                break
        if choice == num:
            for item in dives:
                self.solve_quest(quest_link=item)
        else:
            self.solve_quest(quest_link=dives[choice])

    def solve_quest(self, quest_link: str):
        self.driver.get(quest_link)
        go_back = self.get_elements_by_time(
            by=By.XPATH, value='//input[@value="Go Back"]'
        )
        self.click_button(go_back)
        submit = self.get_elements_by_time(
            by=By.XPATH, value='//input[@value="Accept Quest"]'
        )
        if submit:
            self.click_button_control(element=submit)
        box = self.get_elements_by_time(
            by=By.XPATH, value='//div[@class="flex-table2"]'
        )
        dives = box.find_elements(By.XPATH, "div") if box else []
        dives = [
            self.get_elements_by_time(by=By.XPATH, value=".//a", base=item)
            for item in dives
        ]
        links = [item for item in dives if "market.php" in item.get_attribute("href")]
        for item in links:
            dives.remove(item)
        for item in dives:
            self.click_button(item)
            lnk = self.get_elements_by_time(
                by=By.XPATH, value="//div[@class='middleit']/a[@target='_blank']"
            )
            self.click_button_control(element=lnk)
            try:
                wait = WebDriverWait(self.driver, 5)
                confirmation_message = wait.until(EC.alert_is_present())
                confirmation_message.accept()
            except TimeoutException:
                pass
            self.driver.execute_script("closePriceChecker();")
        self.wait(30)
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
        but = self.get_elements_by_time(
            by=By.XPATH, value='//input[@value="Complete Quest"]'
        )
        self.click_button(element=but)
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        self.wait(10)
        self.solve_quest(quest_link=quest_link)
