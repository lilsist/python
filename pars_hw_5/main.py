from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pymongo
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)

db = client['mvideo']
top_products = db.top_products_01_08

s = Service("./chromedriver_copy")

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(30)

driver.get('https://www.mvideo.ru')
print('ok')

driver.execute_script("window.scrollTo(0, 1500);")
print('ok')
time.sleep(25)

button_trend = driver.find_element(By.XPATH, '//button[contains(@class, "tab-button ng-star-inserted")]')
button_trend.click()
time.sleep(15)
print('ok')

num_goods = int(driver.find_element(
    By.XPATH,
    '//button[contains(@class, "tab-button ng-star-inserted selected")]/div/span[@class="count"]'
).text)
print(num_goods)


goods = driver.find_elements(By.XPATH, '//div[@class="product-mini-card__name ng-star-inserted"]')
for good in goods[:num_goods]:
    products = {}
    prod_name = good.find_element(By.CLASS_NAME, 'title').text
    link = good.find_element(By.TAG_NAME, 'a').get_attribute('href')
    products['prod_name'] = prod_name
    products['link'] = link
    top_products.insert_one(products)
