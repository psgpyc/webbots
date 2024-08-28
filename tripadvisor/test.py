from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from selenium.common.exceptions import WebDriverException

## Define Your Proxy Endpoints
proxy_options = {
    'proxy': {
        'http': 'https://wklvhvaj:rp09d4dezg8t@64.64.118.149:6732',
        
    }
}
options = Options()
options.add_experimental_option('detach', True)

## Set Up Selenium Chrome driver
driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
            seleniumwire_options=proxy_options
        )


## Send Request Using Proxy
driver.get('http://www.google.com')
