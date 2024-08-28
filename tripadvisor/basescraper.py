from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from selenium.common.exceptions import WebDriverException

# List of proxies
proxies = [
    '64.64.118.149:6732:wklvhvaj:rp09d4dezg8t'
]

def test_proxy(proxy, max_retries=3):
    ip, port, username, password = proxy.split(':')
    
    seleniumwire_options = {
        'proxy': {
            'http': f'https://{username}:{password}@{ip}:{port}',
            'https': f'https://{username}:{password}@{ip}:{port}'
        },
        'verify_ssl': False
    }
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    for attempt in range(max_retries):
        driver = None
        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options,
                seleniumwire_options=seleniumwire_options
            )
            driver.set_page_load_timeout(60)
            driver.get('https://api.ipify.org')
            ip = driver.find_element('tag name', 'pre').text
            print(f"Successful connection using proxy: {proxy}")
            print(f"Current IP: {ip}")
            driver.quit()
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for proxy {proxy}: {str(e)}")
            if driver:
                driver.quit()
            time.sleep(random.uniform(1, 3))
    print(f"All attempts failed for proxy {proxy}")
    return False

def main():
    working_proxies = []
    for proxy in proxies:
        if test_proxy(proxy):
            working_proxies.append(proxy)
        time.sleep(random.uniform(2, 5))
    
    print(f"\nWorking proxies: {len(working_proxies)}/{len(proxies)}")
    for proxy in working_proxies:
        print(proxy)

    # Example of using a working proxy for scraping
    if working_proxies:
        proxy = random.choice(working_proxies)
        ip, port, username, password = proxy.split(':')
        
        seleniumwire_options = {
            'proxy': {
                'http': f'https://{username}:{password}@{ip}:{port}',
                'https': f'https://{username}:{password}@{ip}:{port}'
            },
            'verify_ssl': False
        }
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options,
            seleniumwire_options=seleniumwire_options
        )
        
        try:
            print(f"\nUsing proxy {proxy} for scraping example:")
            driver.get('https://example.com')
            print(f"Title of example.com: {driver.title}")
            # Add your scraping logic here
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
        finally:
            driver.quit()
    else:
        print("No working proxies found.")

if __name__ == "__main__":
    main()