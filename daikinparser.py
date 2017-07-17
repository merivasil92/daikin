__author__ = 'motspan'

import requests
from bs4 import *

def main():
    web_get_data()
    save_to_db()

def save_to_db():
    print('Save to DB')

def web_get_data():
    url = 'http://daikin4you.ru'
    res = requests.get(url)
    res.raise_for_status()
    noStarchSoup = BeautifulSoup(res.text, "html.parser")
    catalog_names = []
    megamenu = noStarchSoup.find('nav', {'class':'megamenu'}).find('ul', recursive=False)
    catalog = megamenu.findAll('li', recursive=False)
    for elem in catalog:
        entry = elem.find('a')
        name = entry.attrs['href']
        catalog_names.append(name)
    with open('result.csv', 'w') as f:
        f.write('category;name;price\n')
        for key in catalog_names:
            url = 'http://daikin4you.ru/{0}?page=all'.format(key)
            print(url)
            res = requests.get(url)
            res.raise_for_status()
            noStarchSoup = BeautifulSoup(res.text, "html.parser")
            variants = noStarchSoup.findAll('form', {'class': 'variants'})
            for elem in variants:
                name = elem.attrs['data-name']
                options = elem.findAll('option')
                if len(options) > 0:
                    price = options[0].attrs['data-price']
                    f.write(key + ';' + name + ';' + price + '\n')

if __name__ == '__main__':
    main()
