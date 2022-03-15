import re
from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
import mysql.connector
import time

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='project')
cursor = cnx.cursor()


print('Hello friend, welcome to my app ...')
time.sleep(2)
print("First make sure you're connected to database")
time.sleep(2)
print("for more comfort, you can use «project» for the database name and «car_datas» for the table's name")
time.sleep(2)
print("create a table with these order : name, color, kilometer, model, price.")


r = requests.get('https://divar.ir/s/iran/auto')
searches = int(input('Please enter the number of searches you want: \n>>> '))

soup = BeautifulSoup(r.text, 'html.parser')

val = soup.find_all('div', attrs={'class': 'post-card-item kt-col-6 kt-col-xxl-4'})
count = 0
while count < searches:
    for v in val:
        next_page = re.findall(r'href=\"(.*)\"><div class=\"kt-post-card__b', str(v))
        check = re.search(r'تومان', str(v.text))

        if check:
            req = requests.get(f'https://divar.ir{next_page[0]}')
            r = re.sub('\u200c', ' ', req.text)
            check_name = re.search(r'<title data-react-helmet=\"true\">(.*?)،', r)
            check_kilometers = re.search(r'<span class=\"kt-group-row-item__title kt-body kt-body--sm\">کارکرد</span><span class=\"kt-group-row-item__value\">(.*?)</span>', r)
            check_model = re.search(r'</span><span class=\"kt-group-row-item__value\">(\d*)</span></div><div class=\"kt-group-row-item kt-group-row-item--info-row\"><span class=\"kt-group-row-item__title kt-body kt-body--sm\">رنگ</span>', r)
            check_color = re.search(r'<span class=\"kt-group-row-item__title kt-body kt-body--sm\">رنگ</span><span class=\"kt-group-row-item__value\">(.*?)</span>', r)
            name = re.findall(r'<h1 class=\"kt-page-title__title kt-page-title__title--responsive-sized\">(.*)</h1>', r)
            if check_name and check_kilometers and check_model and check_color:
                count += 1
                kilometers = re.findall(r'<span class=\"kt-group-row-item__title kt-body kt-body--sm\">کارکرد</span><span class=\"kt-group-row-item__value\">(.*?)</span>', r)
                model = re.findall(r'</span><span class=\"kt-group-row-item__value\">(\d*)</span></div><div class=\"kt-group-row-item kt-group-row-item--info-row\"><span class=\"kt-group-row-item__title kt-body kt-body--sm\">رنگ</span>', r)
                price = re.findall(r'\d+٬\d+٬\d+', r)
                color = re.findall(r'<span class=\"kt-group-row-item__title kt-body kt-body--sm\">رنگ</span><span class=\"kt-group-row-item__value\">(.*?)</span>', r)
                new_price = re.sub(',', '.', unidecode(price[0]))
                new_kilometer = re.sub(',', '.', unidecode(kilometers[0]))
                print(f'---- {count} ----')
                print(f"name: {name[0]}, worked kilometers: {new_kilometer}, color: {color[0]}, proce {new_price} Toman.")
                cursor.execute("INSERT INTO car_datas VALUES ('%s', '%s', '%s', '%s', '%s')" % (name[0], color[0], new_kilometer, unidecode(model[0]), new_price))
                cnx.commit()
                if count == searches:
                    time.sleep(1)
                    print(f'\n\n\n {count} datas successfully saved to database !')
                    print('now please open ML project.')
                    break

cnx.close()
