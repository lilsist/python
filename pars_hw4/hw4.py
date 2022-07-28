from lxml import html
import requests
import pymongo
from pymongo import MongoClient
# from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['lenta_ru']
news_lenta = db.news_lenta_29_07

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

url = 'https://lenta.ru'

session = requests.Session()
response = session.get(url, headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//a[contains(@class, '_topnews')]")
for item in items:
    data_dict = {}
    href = item.xpath('.//@href')[0]
    source_list_split = href.split("://")
    text_list = item.xpath('.//text()')
    name, time = text_list[0], text_list[1]
    if len(source_list_split) == 2:
        source = 'https://' + source_list_split[1].split('/')[0]
        href = href
    else:
        source = url
        href = source + href
    data_dict['source'] = source
    data_dict['href'] = href
    data_dict['name'] = name
    data_dict['time'] = time
    news_lenta.insert_one(data_dict)
