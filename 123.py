import requests
from bs4 import BeautifulSoup

page = 0
payload = {'text': 'python',
           'metro': '6',
           'page': str(page)}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
url = 'https://hh.ru/search/vacancy'


def get_jobs():
    r = requests.get(url, headers=headers, params=payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    mydivs = soup.find_all("div", { "class" : "search-result-description__item_primary" })
    print('====== New Page =======')
    for item in mydivs:
        title = item.select_one('.search-result-item__head').find('a')
        money = item.select_one('.b-vacancy-list-salary')
        res = title.string + "   "
        if money:
            res += "   "
            res += money.string
        info = item.select_one('.search-result-item__info')
        if info:
            station = info.select_one('.metro-station')
            if station:
                res += "   "
                res += station.text
        print(res)
    if len(mydivs) == 0:
        return False
    return True

while True:
    a = get_jobs()
    page += 1
    payload = {'text': 'python',
           'metro': '6',
           'page': str(page)}
    if not a:
        break
