import requests
import unittest
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

def is_even(number):
    ''' Returns True if **number** is even or False if it is odd. '''
    return number % 2

class FirstTestCase(unittest.TestCase):
    def even_ints(self):
        self.assertEqual(True, is_even(2))
        self.assertEqual(False, is_even(3))

a = FirstTestCase()
a.even_ints()



res_query = Product.objects.filter(Q(sku__contains = q) | Q(name__contains = q) | Q(description__contains = q))
res_json = serializers.serialize('json', res_query)
return HttpResponse(res_json, content_type='application/json')

# while True:
#     a = get_jobs()
#     page += 1
#     payload = {'text': 'python',
#            'metro': '6',
#            'page': str(page)}
#     if not a:
#         break

r = requests.get('https://www.python.org/')
soup = BeautifulSoup(r.text, 'html.parser')
needed_div = soup.select_one(".shrubbery")

for item in needed_div.find_all('li'):
    print(item.find('a').string)
