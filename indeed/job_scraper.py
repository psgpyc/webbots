import sys
sys.path.append("..")

from indeed import BaseScraper



class JobScraper(BaseScraper):
    def __init__(self, url):
        super().__init__(url)

    def execute(self):
        driver = self.hit_and_wait()
        
        
        
    


js= JobScraper('https://www.google.com')
