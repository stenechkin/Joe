import requests
from bs4 import BeautifulSoup
import urllib3  # игнорирование ошибок сертификата в https

urllib3.disable_warnings()

url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
r = requests.get(url, verify=False, )

with open('main.html', 'w', encoding='utf8') as output_file:
    output_file.write(r.text)

with open("main.html", "r", encoding='utf8') as in_file:
    main_page_text = in_file.read()

soup = BeautifulSoup(main_page_text, features="lxml")

url_list = soup.find_all('a', {'class': 'mzr-tc-group-item-href'})

for number, url_element in enumerate(url_list[38::]):
    href = url_element.get('href')
    url_name = url_element.text

    r = requests.get('https://health-diet.ru{}'.format(href), verify=False, )

    with open('second.html', 'w', encoding='utf8') as output_file:
        output_file.write(r.text)

    in_file = open("second.html", "r", encoding='utf8')
    page_text = in_file.read()
    in_file.close()

    soup2 = BeautifulSoup(page_text, "lxml")

    table = soup2.find('div', {'class': 'uk-overflow-container'})

    if table:
        table = table.find_all('tr')
        print(len(table))

        db = []
        for element in table[1::]:
            line = element.find_all('td')
            if len(line)>3:
                db.append([line[0].text.replace('\n', ''), line[1].text, line[2].text, line[3].text, line[4].text])

        if number == 0:
            mode = 'w'
        else:
            mode = 'a'
        output_file = open('result.csv', mode, encoding='utf8')
            # output_file.write('{}\n'.format(url_name))
        for i in db:
            output_file.write('{};{};{};{};{};{} \n'.format(url_name, i[0], i[1], i[2], i[3], i[4]))
        output_file.close()
