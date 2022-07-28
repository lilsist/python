import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
from pymongo import errors
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['hh']
vacancies = db.vacancies


#vacancy_descr = input("Введите описание вакансии: ")
vacancy_descr = 'Python'

url = 'https://hh.ru/search/vacancy'
params = {'page': '0', 'text': f'{vacancy_descr}', 'items_on_page': 20, 'only_with_salary': 'true'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
session = requests.Session()
response = session.get(url, params=params, headers=headers)
# https://hh.ru/search/vacancy?only_with_salary=true&text=Python&items_on_page=20&page=0
# мы сходили как бы сюда
dom = BeautifulSoup(response.text, 'html.parser')

pager_block = dom.find('div', {'class': 'pager', 'data-qa': 'pager-block'})
num_pages = int(pager_block.find_all('a', {'rel': 'nofollow'})[-2].text)

for page in range(num_pages):
#for page in [0, 1]:
    print(f'scrapping page: {page}')
    params['page'] = page
    response = session.get(url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vac_list = dom.find_all('div', ({'class': 'vacancy-serp-item-body__main-info'}))
    for vac in vac_list:
        data_dict = {}
        vac_name = vac.find('a', ({'target': '_blank'})).text
        salary_list = vac.find('span', ({'class': 'bloko-header-section-3'})).text.split(' ')
        salary_list = [elem.replace('\u202f', '') for elem in salary_list]

        if salary_list[1] == '–':
            salary_min = int(salary_list[0])
            salary_max = int(salary_list[2])
        elif salary_list[0] == 'до':
            salary_min = None
            salary_max = int(salary_list[1])
        elif salary_list[0] == 'от':
            salary_min = int(salary_list[1])
            salary_max = None
        currency = salary_list[-1]
        href = vac.find('a', ({'data-qa': 'vacancy-serp__vacancy-title'})).get('href')

        data_dict['vac_name'] = vac_name
        data_dict['salary_min'] = salary_min
        data_dict['salary_max'] = salary_max
        data_dict['currency'] = currency
        data_dict['href'] = href
        data_dict['host'] = 'hh.ru'

        result = vacancies.find_one({'href': href})

        if result is None:
            vacancies.insert_one(data_dict)
            #print('Добавлена новая вакансия')


# 2 Написать функцию, которая производит поиск и выводит на экран вакансии с
# заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты)

money_filter = 550000
result = vacancies.count_documents({'$or': [
    {'$and': [{'currency': 'руб.'}, {'salary_min': {'$gt': money_filter}}]},
    {'$and': [{'currency': 'руб.'}, {'salary_max': {'$gt': money_filter}}]}
]})
print('Найдено вакансий: ', result)


for item in vacancies.find({'$or': [
    {'$and': [{'currency': 'руб.'}, {'salary_min': {'$gt': money_filter}}]},
    {'$and': [{'currency': 'руб.'}, {'salary_max': {'$gt': money_filter}}]}
]}):
    pprint(item)

client.close()


