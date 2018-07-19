from Services.URLParser import URL
from urllib.parse import quote_plus
from urllib.request import urlopen
#from lxml.html import parse
from bs4 import BeautifulSoup
import requests
import json

# Открыть url для парсинга по ссылке
def OpenURL(url):
    try:
        htmlText = urlopen(url).read()
        strhtml = htmlText.decode('utf-8', errors='ignore')
        # Для тестирования
        with open('URLtest.html', "w", encoding='utf-8') as f:
            f.write(strhtml)
        return strhtml
    except Exception as e:
        print('#bug: ' + str(e))
        return '#bug: ' + str(e)

def OpenURL2(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        r = requests.get(url, headers = headers)
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(r.text) #.decode('cp1251'))
        return r.text
    except Exception as e:
        print('#bug: ' + str(e))
        return '#bug: ' + str(e)

def getLocation(FullAddress, bgoogle=True):
    sGoogle = 'http://maps.google.com/maps/api/geocode/json?sensor=false&address='
    sYandex = 'http://geocode-maps.yandex.ru/1.x/?format=json&geocode='
    geoCodeURL = (sGoogle if bgoogle else sYandex) + quote_plus(FullAddress)
    data = URL.GetData(geoCodeURL)
    geoCodeJson = json.loads(data)
    geoCodeLocation = geoCodeJson['results'][0]['geometry']['location']
    return data

def cln(text):
    text = text.replace('\n','')
    text = text.strip()
    return text

def Parse(text):
    soup = BeautifulSoup(text, 'lxml')
    print(True)
    #Qlist = soup.find('div', {'id': 'bodyconstraint'})
    Qlist = soup.find('div', {'id': 'hotellist_inner'})
    if len(Qlist) > 0:
        print(True)
        soup = BeautifulSoup(str(Qlist), 'xml')
        for item in soup.find_all('div', {'class': 'sr_item_content sr_item_content_slider_wrapper '}):
            sitem = str(item)
            soupl = BeautifulSoup(sitem, 'lxml')
            name = soupl.find('span', {'class': 'sr-hotel__name'}).text
            print(cln(name))
            score = soupl.find('span', {'class': 'review-score-badge'})
            if score:
                print('Оценка: ' + cln(score.text))
            price = soupl.find('strong', {'class': 'price availprice no_rack_rate '})
            if price:
                print('Стоимость: ' + cln(price.text))
            #link = soupl.find('a', {'class': 'hotel_name_link url'}).get('href')
            #print(link)
            print()

    return True

# код для тестирования
#stest = input('Введите тестовую фразу: ')
#url = 'https://www.booking.com/searchresults.ru.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGjCAYgBAZgBIbgBBsgBDNgBAegBAfgBC5ICAXmoAgM&sid=d56929b1fbe6e07b44cd1d51464fe38f&ac_selected=0&checkin_month=4&checkin_monthday=8&checkin_year=2018&checkout_month=4&checkout_monthday=9&checkout_year=2018&city=-2928280&class_interval=1&dest_id=-2980155&dest_type=city&dtdisc=0&from_sf=1&group_adults=1&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A&sb_price_type=total&search_selected=1&src_elem=sb&ss=%D0%9F%D0%B5%D1%80%D0%BC%D1%8C%2C%20%D0%9F%D0%B5%D1%80%D0%BC%D1%81%D0%BA%D0%B8%D0%B9%20%D0%BA%D1%80%D0%B0%D0%B9%2C%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F&ss_all=0&ss_raw=Gthv&ssb=empty&sshis=0&ssne_untouched=%D0%9A%D0%B8%D1%80%D0%BE%D0%B2&order=price'

params = {'checkin_month':'4','checkin_monthday':'8','checkin_year':'2018',
                  'checkout_month':'4','checkout_monthday':'9','checkout_year':'2018',
                  'dest_type':'city','group_adults':'1','group_children':'0',
                  'order':'price','raw_dest_type':'city','sb_price_type':'total',
                  'ss_all':'0','ssb':'empty','sshis':'0'}
url = URL.GetURL('https://www.booking.com/searchresults.ru.html', stext='Грозный', textparam='ss', params=params)
print(url)

text = OpenURL2(url)
if text[0] != '#':
    Parse(text)
    
#print(getLocation(stest))

import time; time.sleep(5)
