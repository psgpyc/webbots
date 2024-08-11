import bs4
import requests
import time
import csv
import random
from helper import get_user_agent, write_to_file


class ThupraiScrapper:
    def __init__(self):
        self.headers = {'User-Agent': get_user_agent()}
        self.title_and_links = []

    def set_url_get_res(self, url):
        return requests.get(url, headers=self.headers)

    def get_soup(self, url, parser='html.parser'):
        response = self.set_url_get_res(url)
        return bs4.BeautifulSoup(response.text, parser)

    def get_title_and_links(self, iter_range):
        for val in range(1, iter_range):
            soup = self.get_soup(url=f'https://thuprai.com/books/nepali?page={val}')
            link_lst = soup.find_all(attrs={"class": "flex flex-col h-full group"})
            for each in link_lst:
                each_book = {'title': each.get('title'), 'link': f"https://thuprai.com{each.get('href')}"}
                self.title_and_links.append(each_book)

            time.sleep(random.randint(2, 6))
            print(val, '.....processed')

        write_to_file(
            title_and_links_list=self.title_and_links,
            file_name='books_title_links_thuprai')







