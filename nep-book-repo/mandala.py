import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from time import sleep
import random

from webdriver_manager.chrome import ChromeDriverManager

from helper import get_user_agent


class MandalaScraper:
    def __init__(self, url):
        self.headers = {'User-Agent': get_user_agent()}
        self.url = url
        self.req = requests.get(self.url, headers=self.headers)

        # setting selenium driver options
        self.options = Options()
        self.selenium_arguments = ("window-size=1400,900", '--silent', '--no-sandbox',
                                   '--disable-notifications', '--disable-dev-shm-usage', '--disable-gpu')

        # running the driver

        # runs the browser in detach mode, prevent the browser from closing automatically when the WebDriver Session is terminated
        self.options.add_experimental_option('detach', True)
        # cleaner console output by limiting logging
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # setting options

        for each in self.selenium_arguments:
            self.options.add_argument(each)

    def hit_and_wait(self, interval=10):
        self.options.headless = True
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.options)
            driver.get(self.url)
        except Exception as e:
            print(f'an error occurred: {e}')

        # driver.maximize_window()

        body_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        body_page.find_element(By.XPATH, '/html/body/header/nav[1]/div/div[2]/ul[2]/div[2]/a').click()


ms = MandalaScraper(url='https://booksmandala.com/books/genres/nepali?view_mode=all&page=1')
ms.hit_and_wait()
