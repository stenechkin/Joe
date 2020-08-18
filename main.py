import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()


class Product(object):
    def __init__(self, product_type, name, calories, protein, fat, carbon):
        self.product_type = product_type
        self.name = name
        self.calories = calories
        self.protein = protein
        self.fat = fat
        self.carbon = carbon
        self.text = f'{product_type}, {name}, {calories}, {protein}, {fat}, {carbon}'

    def get_text_string(self, delimiter=';'):
        return f'{self.product_type}{delimiter}{self.name}{delimiter}{self.calories}{delimiter}{self.protein}' \
               f'{delimiter}{self.fat}{delimiter}{self.carbon}'


url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
r = requests.get(url, verify=False, )
page_text = r.text

# with open('main.html', 'w', encoding='utf8') as output_file:
#     output_file.write(r.text)
#
# with open("main.html", "r", encoding='utf8') as in_file:
#     page_text = in_file.read()

soup = BeautifulSoup(page_text, features="lxml")

url_list = soup.find_all('a', {'class': 'mzr-tc-group-item-href'})

db = []
for number, url_element in enumerate(url_list[0:3:]):
    href = url_element.get('href')
    url_name = url_element.text

    r = requests.get(f'https://health-diet.ru{href}', verify=False, )
    page_text = r.text

    # with open('second.html', 'w', encoding='utf8') as output_file:
    #     output_file.write(r.text)
    #
    # with open("second.html", "r", encoding='utf8') as in_file:
    #     page_text = in_file.read()

    soup = BeautifulSoup(page_text, "lxml")

    table = soup.find('div', {'class': 'uk-overflow-container'})

    if table:
        table = table.find_all('tr')
        print(len(table))

        for element in table[1::]:
            line = element.find_all('td')
            if len(line) > 3:
                db.append(Product(url_name, line[0].text.replace('\n', ''), line[1].text, line[2].text, line[3].text,
                                  line[4].text))

with open('result.csv', 'w', encoding='utf8') as output_file:
    output_file.write('product_type; name; calories; protein; fat; carbon\n')
    for i in db:
        # print(i.get_text_string())
        output_file.write(f'{i.get_text_string()}\n')
