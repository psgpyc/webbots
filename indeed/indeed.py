import sys
sys.path.append("..")

import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import NoSuchElementException, TimeoutException


from webdriver_manager.chrome import ChromeDriverManager

from helpers.helper import get_user_agent


class BaseScraper:
    def __init__(self, url):
        self.headers = {'User_Agent': get_user_agent()}
        self.url = url
        self.req = requests.get(self.url, headers=self.headers)

        #setting selenium driver options
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

    def perform_search(self, body, title, location, driver):
        search_bar_title = body.find_element(By.ID, 'text-input-what')
        search_bar_city = body.find_element(By.ID, 'text-input-where')

        actions = ActionChains(driver)

        actions.move_to_element(search_bar_title).click()
        time.sleep(2)
      
        for each in f"{title}":
            actions.send_keys(each).pause(0.5)

        actions.move_to_element(search_bar_city).click()
        for each in f" {location}":
            actions.send_keys(each).pause(0.5)

        actions.perform()

        time.sleep(2)

        button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'yosegi-InlineWhatWhere-primaryButton')))
        button.click()

    def get_job_results(self, driver):
        job_links = []

        # find the div that contains cards with job descriptions
        div_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div[2]/div/div[5]/div/div[1]/div[5]/div/ul')))
        li = div_result.find_elements(By.CSS_SELECTOR, '.job_seen_beacon')

        for each in li:
            time.sleep(2)
            job_links.append(each.find_element(By.TAG_NAME, 'a').get_attribute('href'))





    def hit_and_wait(self, interval=10):
        self.options.headless = True
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.options)
            driver.get(self.url)
        except Exception as e:
            print(f'an error occurred: {e}')

        driver.maximize_window()
        try:
            body_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        except (NoSuchElementException, TimeoutException):
            print('Element body could not be located')

        self.perform_search(body=body_page, title='python', location='london' ,driver=driver)
        self.get_job_results(driver=driver)

              

        
indeed = BaseScraper(url='https://uk.indeed.com/')
indeed.hit_and_wait()