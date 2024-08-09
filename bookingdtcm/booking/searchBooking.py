import os
from selenium import webdriver
import time
import booking.constants as const
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select



class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\Users\psgpy\PycharmProjects\bookingWebBot\chrome-win64", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += os.pathsep + driver_path
        super(Booking, self).__init__()

        # self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.close()
        else:
            time.sleep(3)

    def land_first_page(self):
        self.get(const.BASE_URL)

    def accept_cookies(self):
        try:
            self.find_element(By.ID, 'onetrust-accept-btn-handler').click()
            return 'success_cookies'

        except:
            print('An error occurred! Please retry in a while: from accept cookies')
            return 'error_cookies'

    def remove_login_popup(self):
        try:
            popup = WebDriverWait(self, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[aria-label='Dismiss sign-in info.']")))

        except:
            print('An error occurred! Please retry in a while: remove login page')
            return 'error'

        popup.click()
        return 'success'


    def change_currency(self, currency):
        el_currency = WebDriverWait(self, 10).until(EC.presence_of_element_located(
                (By.XPATH,"//SPAN[@class='eed450ee2f']")))
        el_currency.click()
        try:
            el_currency_select = self.find_element(By.XPATH, f"//div[text()='{currency}']")
            el_currency_select.click()

        except Exception as e:
            print(e)

    def select_vacation_destination(self, address):
        try:
            el_address = self.find_element(By.XPATH, "//input[@name='ss']")
            el_address.send_keys(address)

            el_dropped_dest = self.find_element(By.XPATH, f"//div[@data-testid='autocomplete-results-options']//div[text() = '{address}']")
            el_dropped_dest.click()
        except Exception as e:
            print(e)

    def select_arrival_date(self, dateval_checkin, dateval_checkout):
        try:

            date_el_checkin = self.find_element(By.XPATH, f"//span[@data-date='{dateval_checkin}']")
            date_el_checkin.click()
            date_el_checkout = self.find_element(By.XPATH, f"//span[@data-date='{dateval_checkout}']")
            date_el_checkout.click()

        except Exception as e:
            print(e)

    def select_occupancy(self):
        try:
            el_adults=self.find_element(
                By.XPATH,
                "//button[@data-testid='occupancy-config']")
            el_adults.click()
        except Exception as e:
            print(e)

    def select_adults(self, adults_number):
        try:
            adult_el = self.find_element(By.XPATH, "//div[@class='f71ad9bb14']")
            decrease_capacity_el = self.find_element(By.XPATH, "//div[@class='f71ad9bb14']/*[1]")
            decrease_capacity_el.click()
            increase_capacity_el = self.find_element(By.XPATH, "//div[@class='f71ad9bb14']/*[3]")
            variance = adults_number - int(adult_el.text)
            if variance > 1:
                for each in range(abs(variance)):
                    increase_capacity_el.click()

        except Exception as e:
            print(e)

    # def select_children_age(self, index_val,age=12):
    #     try:
    #         age_input_elem =
    #         age_input_elem.click()
    #     except:
    #         print('An error occurred!', index_val+1)

    def select_children(self, children_number):
        if children_number > 0:
            children_el = self.find_element(By.XPATH, "//DIV[@class='abb8c87649']/*[2]/*[3]/*[3]")
            for i in range(children_number):
                children_el.click()
        for each_children in range(children_number):

            elem = self.find_element(By.XPATH, f"//DIV[@class='abb8c87649']//DIV[@data-testid='kids-ages']")
            for each in elem.get_attribute('outerHTML'):
                print(each)

    def select_no_of_rooms(self, no_of_rooms):
        if no_of_rooms > 1:
            room_el = self.find_element(By.XPATH, "//DIV[@class='abb8c87649']/DIV[@class='f340be2edd'][3]/*[3]/*[3]")
            for i in range(no_of_rooms - 1):
                room_el.click()


