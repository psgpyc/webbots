import bs4
import requests
import time
import csv
import random

final_list = []

for val in range(1,136):
    res = requests.get(f'https://thuprai.com/books/nepali?page={val}')

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    link_lst = soup.find_all(attrs={"class": "flex flex-col h-full group"})
    for each in link_lst:
        each_book = {'title':each.get('title'), 'link': f"https://thuprai.com/{each.get('href')}" }
        final_list.append(each_book)
    
    time.sleep(random.randint(2,6))
    print(val, '.....processed')

csv_file = 'output.csv'
fieldnames = final_list[0].keys()

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the rows
    for row in final_list:
        writer.writerow(row)
