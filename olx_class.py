import requests
from bs4 import BeautifulSoup
import csv


class Scraper:
    def __init__(self):
        self.url = 'https://www.olx.ua/elektronika/q-macbook-pro-2015/?page=1'
        self.base_url = 'https://www.olx.ua/elektronika/'
        self.query_part = 'q-macbook-pro-2015/'
        self.page_part = '?page='
        self.total_pages = self.get_total_pages(self.get_html(self.url))
        self.ad_ids = []
        self.csvfile = open('olx.csv', 'a', newline='')
        self.fieldnames = ['Название', 'Цена', 'Город', 'Ссылка']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)

    @staticmethod
    def get_html(url):
        r = requests.get(url)
        return r.text

    @staticmethod
    def get_total_pages(html):
        soup = BeautifulSoup(html, 'lxml')
        pages = soup.find('div', class_='pager rel clr').find_all('a', class_='block br3 brc8 large tdnone lheight24')[
            -1].get('href')
        total_pages = pages.split('=')[1]
        return int(total_pages)

    def get_page_data(self, html):
        soup = BeautifulSoup(html, 'lxml')
        ads = soup.find('div', class_='listHandler').find_all('div', class_='offer-wrapper')
        for ad in ads:
            try:
                title = ad.find('div', class_='space rel').find('strong').get_text().split(",")[0]
            except:
                title = ''
            try:
                url = ad.find('div', class_='space rel').find('h3', class_='lheight22 margintop5').find('a').get(
                    'href').split(",")[0]
            except:
                url = ''
            try:
                price = \
                    ad.find('div', class_='space inlblk rel').find('p', class_='price').get_text().strip().split(",")[0]
            except:
                price = ''
            try:
                geo = ad.find_all('p', class_='lheight16')[1].text.strip().split(",")[0]
                geo = ''.join(geo.split()[0])
            except:
                geo = ''
            try:
                ad_id = ad.find('table').get_attribute_list('data-id')[0]
                if ad_id in self.ad_ids:
                    continue
                self.ad_ids.append(ad_id)
            except:
                pass
            data = {'title': title,
                    'price': price,
                    'geo': geo,
                    'url': url, }
            self.write_csv(data)

    def write_csv(self, data):
        self.writer.writerow(
            {'Название': data['title'], 'Цена': data['price'], 'Город': data['geo'], 'Ссылка': data['url']})

    def run(self):
        self.writer.writeheader()
        for i in range(1, self.total_pages + 1):
            url_gen = self.base_url + self.query_part + self.page_part + str(i)
            html = self.get_html(url_gen)
            self.get_page_data(html)
        self.csvfile.close()


scraper = Scraper()
scraper.run()