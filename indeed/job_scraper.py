import sys
sys.path.append("..")


import time
import requests

from indeed import BaseScraper
from helpers.helper import read_links_from_csv


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import NoSuchElementException, TimeoutException


from webdriver_manager.chrome import ChromeDriverManager



class JobScraper(BaseScraper):
    filepath = 'indeed_links.csv'

    def __init__(self):
        self.url = read_links_from_csv(file_path=JobScraper.filepath, index=0)[0]

        super().__init__(self.url)

    def check_body_tag_exists(self, driver):
        exists = True
        try:
            body_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        except (NoSuchElementException, TimeoutException):
            print('Element body could not be located')
            exists = False
        return exists, body_page

    def get_job_title(self, body):
        try:
            title_h1 = body.find_element(By.CSS_SELECTOR, 'h1.jobsearch-JobInfoHeader-title.css-1b4cr5z.e1tiznh50 span')
            title = title_h1.text
            return title
        except NoSuchElementException:
            print("Error: Could not find the job title element on the page.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while getting the job title: {str(e)}")
            return None
    
    def get_company_name_address(self, body):
        try:
            company_info_container = body.find_element(By.CSS_SELECTOR, 'div[data-testid="jobsearch-CompanyInfoContainer"]')

            #extract company name
            company_name_element = company_info_container.find_element(By.CSS_SELECTOR, 'div[data-company-name="true"]')

            company_name = company_name_element.text.strip()

            # Extract company address
            company_address_element = company_info_container.find_element(By.CSS_SELECTOR, 'div[data-testid="job-location"]')
            company_address = company_address_element.text.strip()

            return company_name, company_address

        except NoSuchElementException:
            print("Error: Could not find the company name and address element on the page.")
            return None, None


    def execute(self):
        driver = self.hit_and_wait()
        body_tag_exists, body = self.check_body_tag_exists(driver)
        if body_tag_exists:
            print(self.get_job_title(body))
            print(self.get_company_name_address(body))

        
        
        
    


js= JobScraper()
js.execute()