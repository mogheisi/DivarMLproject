import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://divar.ir/s/tehran')
print(r)

soup = BeautifulSoup(r.text, 'html.parser')

val = soup.find_all('div', attrs={'class': "kt-post-card__body"})

for v in val:
    found = re.search(r"توافقی", v.text)
    if found:
        print(' : قیمت ثبت شده آگهی با عنوان زیر در صفجه اول دیوار تهران توافقی است ')
        print('\033[1m\n', found.string, '\n\n\n')
