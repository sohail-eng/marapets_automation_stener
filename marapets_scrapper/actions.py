import getpass
import os
import pickle
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from . import constants as c

BASE_URL = "https://www.marapets.com/"


def __prompt_email_password():
    u = input("User Name: ")
    p = getpass.getpass(prompt="Password: ")
    return u, p


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def load_cookies(driver):
    driver.get(BASE_URL)
    if os.path.isfile(c.COOKIE_FILE_NAME):
        with open(c.COOKIE_FILE_NAME, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.get(f'{BASE_URL}')
        sleep(2)


def action_click(driver, element):
    action = ActionChains(driver)
    action.click(element)
    action.perform()


def save_cookies(driver):
    pickle.dump(driver.get_cookies(), open(c.COOKIE_FILE_NAME, 'wb'))


def login(driver, email=None, password=None, timeout=10):
    load_cookies(driver=driver)
    counter = 0
    while counter < 5:
        elements = driver.find_elements(By.XPATH, c.VERIFY_LOGIN_ID)
        if elements:
            return
        counter = counter + 1
        sleep(2)

    if not email or not password:
        email, password = __prompt_email_password()

    driver.get(f"{BASE_URL}login.php")

    try:
        email_elem = driver.find_element(By.ID, "username")
        email_elem.send_keys(email)
    except NoSuchElementException:
        pass
    except Exception as e:
        pass
    sleep(2)
    try:
        submit_elem = driver.find_element(By.XPATH, "//input[contains(@value,'Login')]")
        action_click(driver=driver, element=submit_elem)
    except NoSuchElementException:
        pass
    except Exception as e:
        pass
    try:
        password_elem = driver.find_element(By.XPATH, "//input[contains(@name,'password')]")
        password_elem.send_keys(password)
        password_elem.submit()
    except NoSuchElementException:
        pass
    except Exception as e:
        pass

    if driver.current_url == f'{BASE_URL}checkpoint/lg/login-submit':
        remember = driver.find_element(By.ID, c.REMEMBER_PROMPT)
        if remember:
            remember.submit()

    counters = 0
    while counters < timeout:
        sleep(1)
        element = driver.find_elements(By.XPATH, c.VERIFY_LOGIN_ID)
        if element:
            break
    save_cookies(driver)
