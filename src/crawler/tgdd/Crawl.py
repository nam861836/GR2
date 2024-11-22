import requests
from bs4 import BeautifulSoup
from time import sleep
from Common import REAL_PATH, PREFIX_PRODUCT_URL, SLEEP_TIME, SAVE_DIR, PRODUCT_INFO_NEED
import os
from os import makedirs
import csv
from playwright.sync_api import sync_playwright


class TGDD_Crawler:
    
    def __init__(self):

        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                } 
        self.ignore = ['javascript:;']
    
    @staticmethod
    def run_playwright(playwright, url):
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        browser.close()
        return content
    
    @staticmethod
    def getHtmlPlayWright(url):
        with sync_playwright() as playwright:
            html = TGDD_Crawler.run_playwright(playwright, url)
            return html

    def _getSoup(self, url):
                
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            print(e)
            return None
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def _crawlLinkProduct(self, url):
        soup = BeautifulSoup(TGDD_Crawler.getHtmlPlayWright(url),'html.parser')
        return [item.get('href') for  item in (soup.find('div', class_='container-productbox').find('ul', class_='listproduct').find_all('a')) if item.get('href') not in self.ignore][0: PRODUCT_INFO_NEED]
    
    def _crawlProductInfo(self, url):
        res = {}
        soup = self._getSoup(url)
        boxs = soup.find_all('div', class_='box-specifi')
        for box in boxs:
            title = box.find_next('a').get_text()
            container = {}
            ul = box.find_next('ul', class_="text-specifi")
            lis = ul.find_all('li')
            for li in lis:
                asides = li.find_all('aside')
                sub_title = asides[0].find_next('strong').get_text()
                content_list = []
                for content in asides[1]:
                    if content == '\n':
                        continue
                    content_list.append(content.get_text())
                container[sub_title] = content_list
            res[title] = container
        return res

    def _crawlProductsInfo(self, url):
        data = []
        urls = self._crawlLinkProduct(url)
        n = len(urls)
        for idx, product_url in enumerate(urls):
            product_url = PREFIX_PRODUCT_URL + product_url
            product_info = self._crawlProductInfo(product_url)
            product_info["URL"] = product_url
            data.append(product_info)
            percent = (idx + 1) / n * 100
            print("Đã hoàn thành:", str(percent) + "%")
            sleep(SLEEP_TIME)
        return data

    def _saveData(self, data):
        makedirs(SAVE_DIR, exist_ok=True)
        file = SAVE_DIR + "//tgdd.csv"
        # Extract headers dynamically from data
        headers = ["URL"] + list(set(key for product in data for key in product.keys() if key != "URL"))
        
        with open(file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for product in data:
                flat_product = {k: ', '.join(v) if isinstance(v, list) else v for k, v in product.items()}
                writer.writerow(flat_product)

    def run(self) -> None:
        self._saveData(self._crawlProductsInfo(REAL_PATH))
