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
        self.url = read_links_from_csv(file_path=JobScraper.filepath, index=0)[722]

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
    
    def get_company_name(self, body):
        try:
            company_info_container = body.find_element(By.CSS_SELECTOR, 'div[data-testid="jobsearch-CompanyInfoContainer"]')

            #extract company name
            company_name_element = company_info_container.find_element(By.CSS_SELECTOR, 'div[data-company-name="true"]')
            company_name = company_name_element.text.strip()

            return company_name

        except NoSuchElementException:
            print("Error: Could not find the company name and address element on the page.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while getting the job title: {str(e)}")
            return None    
        
    def get_salary(self, body):
        try:
            # Wait for the salary and job type container to be present
            info_container = body.find_element(By.ID, "salaryInfoAndJobType")
            

            # Extract salary
            salary_element = info_container.find_element(By.CSS_SELECTOR, "span.css-19j1a75")
            salary = salary_element.text

            return salary
        except NoSuchElementException:
            print("Error: Could not find the salary element on the page.")
            return None

        except Exception as e:
            print(f"An error occurred while extracting salary", e)
            return None
    
    def get_job_type(self, body):
        try:
            # Wait for the salary and job type container to be present
            info_container = body.find_element(By.ID, "salaryInfoAndJobType")
            

            # Extract salary
            job_type_element = info_container.find_element(By.CSS_SELECTOR, "span.css-k5flys")
            job_type = job_type_element.text

            return job_type
        
        except NoSuchElementException:
            print("Error: Could not find the job type element on the page.")
            return None

        except Exception as e:
            print(f"An error occurred while extracting job_type", e)
            return None
        
    def get_job_location(self, body):
        try:
            location_container = body.find_element(By.ID, 'jobLocationWrapper')
            try:
                location_elem = location_container.find_element(By.CSS_SELECTOR, "div[data-testid=jobsearch-JobInfoHeader-companyLocation]")
            except NoSuchElementException:
                location_elem = location_container.find_element(By.CSS_SELECTOR, "div[data-testid='job-location']")
            return location_elem.text

        except NoSuchElementException:
            print("Error: Could not find the company address element on the page.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while getting the address element:", str(e))
            return None     
        
    def get_section_wrapper(self, body, id):
        # check if a particular block exists. eg: Job Details,  Benefit, Full Job Description
        try:
            wrapper_elem = body.find_element(By.ID, id)
            return wrapper_elem

        except NoSuchElementException:
            print('Profile BLock element( Job Details,  Benefit) not found')
            return None

    def extract_from_job_details_section_wrapper(self, body, profile_insights_wrapper):

        # extract group roles for each div in insights wrapper above
        job_details = {
            'Job type' : None,
            'Shift and schedule': None
        }

        try:
            group_divs = profile_insights_wrapper.find_elements(By.CSS_SELECTOR, "div[role='group']")
            if len(group_divs) > 0:
                for each in group_divs:
                    list_elem = each.find_elements(By.CSS_SELECTOR, 'li.js-match-insights-provider-hj3618.eu4oa1w0')
                    job_details[each.get_attribute('aria-label')] = [elem.text for elem in list_elem]       

                return job_details
            else:
                print('group roles do not exist')
                return job_details
        except NoSuchElementException:
            print('Couldnot locate role divs')
            return job_details
        
    def extract_benefits(self, benefit_wrapper):
        benefit_details = {
            'benefits': None
        }
        
        try:
            benefits_li_elem = benefit_wrapper.find_elements(By.CSS_SELECTOR, 'li.css-kyg8or.eu4oa1w0')

            benefit_details['benefits'] = [elem.text for elem in benefits_li_elem]
            return benefit_details
        except NoSuchElementException:
            print('no benefit element located')
            return benefit_details
        
    def extract_text_from_li(self, ul_elem):
        try:
            li_elem = ul_elem.find_elements(By.TAG_NAME, 'li')
            return [li.text for li in li_elem]
        except NoSuchElementException:
            print('no li element exists')

        
    def extract_job_description(self, wrapper, driver):
        job_description = {}
        try:
            ul_list = wrapper.find_elements(By.TAG_NAME, 'ul')

            for each in ul_list:
                previous_sibling = each.find_element(By.XPATH, "./preceding-sibling::*[1]")
                job_description[previous_sibling.text] = self.extract_text_from_li(ul_elem=each)

            return job_description

            
        except NoSuchElementException:
            print('unable to locate job description ul elems')
            return job_description        

    def execute(self):
        extracted_details = {} 
        driver = self.hit_and_wait()
        body_tag_exists, body = self.check_body_tag_exists(driver)
        if body_tag_exists:

            extracted_details['job_title'] = self.get_job_title(body)
            extracted_details['company_name'] = self.get_company_name(body)
            extracted_details['salary'] = self.get_salary(body)
            extracted_details['job_location'] = self.get_job_location(body)
            job_details_wrapper = self.get_section_wrapper(body=body, id='mosaic-vjJobDetails')
            if job_details_wrapper:
                extracted_details['job_details'] = self.extract_from_job_details_section_wrapper(body, job_details_wrapper)
            benefits = self.get_section_wrapper(body=body, id='benefits')
            if benefits:
                extracted_details['benefits'] = self.extract_benefits(benefit_wrapper=benefits)
            full_job_description = self.get_section_wrapper(body=body, id="jobDescriptionText")
            extracted_details['job_description'] = self.extract_job_description(wrapper=full_job_description, driver=driver)

        print(extracted_details)
           


js= JobScraper()
js.execute()