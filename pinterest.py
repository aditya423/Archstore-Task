import sys
import re
import json
import os
import cv2
import numpy as np
import csv

from requests import get
from tqdm import tqdm
from bs4 import BeautifulSoup as soup
from concurrent.futures import ThreadPoolExecutor
from pydotmap import DotMap


class PinterestImageScraper:

    def __init__(self):
        self.json_data_list = []
        self.unique_img = []

    # ---------------------------------------- GET GOOGLE RESULTS ---------------------------------
    @staticmethod
    def get_pinterest_links(body):
        searched_urls = []
        html = soup(body, 'html.parser')
        links = html.select('#main > div > div > div > a')
        print('[+] saving hyperlinks ...')
        for link in links:
            link = link.get('href')
            link = re.sub(r'/url\?q=', '', link)
            if link[0] != "/" and "pinterest" in link:
                searched_urls.append(link)

        return searched_urls

    # -------------------------- save json data from source code of given pinterest url -------------
    def get_source(self, url):
        try:
            res = get(url)
        except Exception as e:
            return
        html = soup(res.text, 'html.parser')
        json_data = html.find_all("script", attrs={"id": "__PWS_DATA__"})
        for a in json_data:
            self.json_data_list.append(a.string)

    # --------------------------- READ JSON OF PINTEREST WEBSITE ----------------------
    def save_image_url(self):
        print('[+] saving image urls to the list...')
        url_list = [i for i in self.json_data_list if i.strip()]
        if not len(url_list):
            return url_list
        url_list = []
        for js in self.json_data_list:
            try:
                data = DotMap(json.loads(js))
                urls = []
                for pin in data.props.initialReduxState.pins:
                    if isinstance(data.props.initialReduxState.pins[pin].images.get("orig"), list):
                        for i in data.props.initialReduxState.pins[pin].images.get("orig"):
                            urls.append(i.get("url"))
                    else:
                        urls.append(data.props.initialReduxState.pins[pin].images.get("orig").get("url"))

                for url in urls:
                    url_list.append(url)
            except Exception as e:
                continue
        
        return list(set(url_list))

    # -------------------------- get user keyword and google search for that keywords ---------------------
    @staticmethod
    def start_scraping(key=None):
        try:
            key = input("Enter pinterest tag to search: ") if key == None else key
            keyword = key + " pinterest"
            keyword = keyword.replace("+", "%20")
            url = f'http://www.google.co.in/search?hl=en&q={keyword}'
            print(f'[+] searching for {key} tag on pinterest...')
            res = get(url)
            searched_urls = PinterestImageScraper.get_pinterest_links(res.content)
        except Exception as e:
            return []

        return searched_urls, key.replace(" ", "_")
    
    # -------------------------- get user keyword and google search for that keywords ---------------------
    def make_ready_csv(self, key=None):

        extracted_urls, keyword = PinterestImageScraper.start_scraping(key)

        print('[+] saving json data...')
        for i in extracted_urls:
            self.get_source(i)

        url_list = self.save_image_url()
        print()
        print(f"Total {len(url_list)} files available")
        print(f"[+] saving image urls into CSV file...")

        with open('urls.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            for link in url_list:
                csvwriter.writerow([link])
        csvfile.close()

        return True


if __name__ == "__main__":
    p_scraper = PinterestImageScraper()
    is_saved = p_scraper.make_ready_csv()

    if is_saved:
        print("\nDone... !")
    else:
        print("\nNothing to save !")
