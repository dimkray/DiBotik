from Services.Yandex import Ya
from Services.URLParser import URL, Parser
import certifi
import urllib3
from urllib.parse import urlencode
from urllib.parse import quote

# Сервис поиска универсальной карты (с маршрутами или обозначениями)
def Search(text):
    text = text.replace(' ','+')
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    req = format(quote(text))
    r = http.request('GET', 'https://www.google.ru/search?q='+req)
    print('https://www.google.ru/search?q='+req)
    if r.status == 200:
        d = r.data.decode('utf-8', 'ignore')
        with open('url.html','w', encoding='utf-8') as f:
            f.write(d)
        f.close()
        start = d.find('https://maps.google.ru/maps?q='+req)
        if start > 0: # если есть признак карты
            end = d.find('"', start + 1)
            ftext = d[start:end]
            return ftext.replace('%2B','%20')
        else:
            print('#bug: none')
            return '#bug: none'
    else:
        return '#porblem: ' + str(r.status_code)

text = input('Введите тестовую фразу: ')

# здесь тестовая обработка #

print(Search(text))

print(URL.GetURL('https://www.google.ru/search',stext=text,textparam='q'))
data = URL.GetData('https://www.google.ru/search',stext=text,textparam='q',brequest=False)
if data[0] != '#':
    with open('url.html','w', encoding='utf-8') as f:
        f.write(data)
    f.close()
    ftext = Parser.Find(data,'https://maps.google.ru/maps?q=',send='"',ball=False)
    if ftext[0] != '#':
        ftext = ftext.replace('%2B','%20')

print('Результат тестирования: ' + ftext)

import time; time.sleep(5)
