import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pager rel clr').find_all('a', class_='block br3 brc8 large tdnone lheight24')[
        -1].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)


def write_csv(data, writes_count):
    with open('olx.csv', 'a', newline='') as csvfile:
        fieldnames = ['Название', 'Цена', 'Город', 'Ссылка']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if writes_count < 1:
            writer.writeheader()
        writer.writerow({'Название': data['title'], 'Цена': data['price'], 'Город': data['geo'], 'Ссылка': data['url']})


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='listHandler').find_all('div', class_='offer-wrapper')
    writes_count = 0
    ids = []
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
            price = ad.find('div', class_='space inlblk rel').find('p', class_='price').get_text().strip().split(",")[0]
        except:
            price = ''
        try:
            geo = ad.find_all('p', class_='lheight16')[1].text.strip().split(",")[0]
            geo = ''.join(geo.split()[0])
        except:
            geo = ''
        try:
            id = ad.find('table').get_attribute_list('data-id')[0]
            ids.append(id)
        except:
            id = ''
        data = {'title': title,
                'price': price,
                'geo': geo,
                'url': url, }
        write_csv(data, writes_count)
        writes_count += 1


def clean_data(data_list, id):
    for ad in data_list:
        if id in ad.get('id'):
            data_list.remove(ad)


def main():
    url = 'https://www.olx.ua/elektronika/q-macbook-pro-2015/?page=1'
    base_url = 'https://www.olx.ua/elektronika/'
    query_part = 'q-macbook-pro-2015/'
    page_part = '?page='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages + 1):
        url_gen = base_url + query_part + page_part + str(i)
        html = get_html(url_gen)
        get_page_data(html)


main()
