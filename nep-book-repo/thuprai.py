import bs4
import requests
import time
import csv
import re
import random
from helper import get_user_agent, write_to_file, read_links_from_csv
from settings import THUPRAI_BASE_URL, ENGLISH_TITLE_CLASS, PRICE_BLOCK, PRICE_DIV, PRICE_SPAN, PUBLISHER_BLOCK, PUBLISER_NAME, ADDITIONAL_DETAILS_ATTRS, ADDITIONAL_DETAILS_ATTRS_EACH

import logging
logging.basicConfig(filename='app.log', level=logging.ERROR)


class ThupraiScrapper:
    def __init__(self):
        self.headers = {'User-Agent': get_user_agent()}

    def set_url_get_res(self, url):
        res = requests.get(url, headers=self.headers)
        return res

    def get_soup(self, url, parser='html.parser'):
        response = self.set_url_get_res(url)
        return bs4.BeautifulSoup(response.text, parser)


class LinksToBooks(ThupraiScrapper):
    def __init__(self):
        super().__init__()
        self.title_and_links = []

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


class BooksDetails(ThupraiScrapper):
    def __init__(self):
        self.links = {}
        super().__init__()

    def get_links(self, filepath):
        self.links['links'] = read_links_from_csv(filepath)
        return self.links

    def get_title_and_author(self, soup):
        result = {}
        try:
            # find the english title
            title_english_elem = soup.find(attrs={"class": ENGLISH_TITLE_CLASS})
            if title_english_elem is None:
                raise ValueError("English title element not found")
            result['title_english'] = title_english_elem.get_text(strip=True)
            # find the nepali title
            title_nepali_elem = title_english_elem.parent.next_sibling
            if title_nepali_elem is None or not hasattr(title_nepali_elem, 'text'):
                raise ValueError("Nepali title element not found.")
            result['title_nepali'] = title_nepali_elem.get_text(strip=True)

            # find the author element
            author_elem = title_nepali_elem.next_sibling.findChildren('a')
            if not author_elem:
                raise ValueError("Author element not found.")

            author_profile_link = f"{THUPRAI_BASE_URL}{author_elem[0].get('href')}"
            author_name = author_elem[0].text

            result['author_profile_link'] = author_profile_link
            result['author_name'] = author_name

        except (AttributeError, ValueError) as e:
            logging.error(f'An error occurred: {str(e)}')
            return {'title_english': None,
                    'title_nepali': None,
                    'author_profile_link': None,
                    'author_name': None}

        return result

    def get_price_details(self, soup):
        # Initialize an empty list to store the results
        result = {}
        try:
            # Find the main price block div using its class name
            price_block = soup.find("div", attrs={
                "class": PRICE_BLOCK})

            # Check if the price block was found; raise an error if not

            if price_block is None:
                raise ValueError("price block element not found")

            # Find all divs within the price block that have a class containing 'color box'
            div_in_price_block = price_block.find_all('div', class_=re.compile(r'\bcolor box\b'))

            # Iterate over each div found within the price block

            for div in div_in_price_block:

                text_parts = div.get_text().split(" ")
                if len(text_parts) > 1:
                    binding_type = text_parts[1]
                else:
                    print("Text split did not contain enough parts")

                price_div = div.find('div', class_=PRICE_DIV)

                # Find the price div within the current div

                if price_div:
                    # Find the span within the price div that contains the price

                    price_span = price_div.find('span', class_=PRICE_SPAN)
                    # Check if the price span was found

                    if price_span:
                        # Find the specific span that contains the book price

                        price = price_span.find('span')
                        if price:
                            book_price = price.get_text(strip=True)
                        else:
                            print("price span not found")
                    else:
                        print(f"price span with class {PRICE_SPAN} not found")
                else:
                    print("price div not found")
                # Append the extracted binding type and price to the result list

                price_dict = {'price':book_price}
                result[binding_type] = price_dict

        except (AttributeError, ValueError) as e:
            # Handle any AttributeErrors that occur during the process

            print('An error occurred', str(e))
        # Return the list of extracted price details

        if len(result) == 0:
            return {'is_pdf': True, 'price': 'free'}
        else:
            return result

    def get_publishers_details(self, soup):
        result = {}
        try:
            publisher_block = soup.find("div", class_=PUBLISHER_BLOCK)
            if publisher_block is None:
                raise ValueError('Publisher block with class mt-5 text-gray-700 not found')

            publisher_link_elem = publisher_block.find("a")
            if publisher_link_elem is not None:
                publisher_profile_link = f"{THUPRAI_BASE_URL}{publisher_link_elem['href']}"
                result['publisher_profile_link'] = publisher_profile_link
            else:
                print('cant locate elem a in Publisher block')

            publisher_name_elem = publisher_block.find("div", class_=PUBLISER_NAME)
            if publisher_name_elem is not None:
                publisher_name = publisher_name_elem.get_text(strip=True)
                result['publisher_name'] = publisher_name
            else:
                print('cant locate elem with the class hover:underline h-fit my-2')

        except (AttributeError, ValueError) as e:
            logging.error('error', str(e))

        return result

    def get_additional_details(self, soup):
        result = {
            'genre': None,
            'published_date': None,
            'edition': None,
            'isbn10': None,
            'isbn13': None,
            'pages': None,
            'weight': None,
            'language': None
        }

        additional_details = soup.find(attrs={"class": ADDITIONAL_DETAILS_ATTRS})

        if additional_details is not None:
            published_on = additional_details.find_all("tr")
            for each in published_on:
                table_heading = each.find("td")
                if table_heading is not None:
                    if table_heading.get_text(strip=True) == 'Genre:':
                        genre = each.find("th", attrs={"class": ADDITIONAL_DETAILS_ATTRS_EACH}).get_text(strip=True)
                        result['genre'] = genre
                    if table_heading.get_text(strip=True) == 'Published:':
                        published_date = each.find("th", attrs={"class": ADDITIONAL_DETAILS_ATTRS_EACH}).get_text(strip=True)
                        result['published_date'] = published_date
                    if table_heading.get_text(strip=True) == 'Edition:':
                        edition = each.find("th", attrs={"class": ADDITIONAL_DETAILS_ATTRS_EACH}).get_text(strip=True)
                        result['edition'] = edition
                    if table_heading.get_text(strip=True) == 'ISBN13:':
                        isbn13 = each.find("th", attrs={"class": ADDITIONAL_DETAILS_ATTRS_EACH}).get_text(strip=True)
                        result['isbn13'] = isbn13
                    if table_heading.get_text(strip=True) == 'ISBN10:':
                        isbn10 = each.find("th", attrs={"class": ADDITIONAL_DETAILS_ATTRS_EACH}).get_text(strip=True)
                        result['isbn10'] = isbn10
                    if table_heading.get_text(strip=True) == 'Pages:':
                        pages = each.find("th", attrs={"class": ADDITIONAL_DETAILS_ATTRS_EACH}).get_text(strip=True)
                        result['pages'] = pages
                    if table_heading.get_text(strip=True) == 'Weight:':
                        weight = each.find("th", attrs={"class": ADDITIONAL_DETAILS_ATTRS_EACH}).get_text(strip=True)
                        result['weight'] = weight
                    if table_heading.get_text(strip=True) == 'Language:':
                        language = each.find("th", attrs={"class": ADDITIONAL_DETAILS_ATTRS_EACH}).get_text(strip=True)
                        result['language'] = language

        return result

    def execute(self):

        links = self.get_links(r'C:\Users\psgpy\PycharmProjects\webbots\nep-book-repo\scrapped-csvs\books_title_links_thuprai.csv')
        url = "https://thuprai.com/magazine/taksar-vol-4-issue-4/"
        if 'taksar' in url:
            return 'taksar found'
        else:
            soup = self.get_soup(url=url)

            title_and_author = self.get_title_and_author(soup)
            binding_and_price = self.get_price_details(soup)
            publisher_details = self.get_publishers_details(soup)
            additional_details = self.get_additional_details(soup)

            return {**title_and_author, 'bindings': binding_and_price, **publisher_details, **additional_details},




bd = BooksDetails()
print(bd.execute())

