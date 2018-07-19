import requests
import certifi
import urllib3
from urllib.parse import urlencode
from urllib.parse import quote

class URL:
    # Возвращает URL
    def GetURL(shttp, stext = '', textparam = '', params = {}):
        stext = stext.replace(' ','+')
        stext = format(quote(stext))
        if len(params) > 0 or len(textparam) > 0:
            if len(textparam) > 0: params[textparam] = stext
        if len(params) > 0:
            req = ''
            for param in params:
                if params[param] is not str: params[param] = str(params[param])
                req += param +'='+ params[param] +'&'
            shttp += '?'+req       
        return shttp
        
    # Получение html/основного текста по запросу
    def GetData(shttp, stext = '', textparam = '', params = {}, brequest = True):
        stext = stext.replace(' ','+')
        stext = format(quote(stext))
        status = 0; d = '' # Данные для ответа
        if brequest: # Если через request
            if len(params) > 0 or len(textparam) > 0:
                if len(textparam) > 0: params[textparam] = stext
                r = requests.get(shttp, params=params)
            else:
                r = requests.get(shttp)
            status = r.status_code
            if status == requests.codes.ok: d = r.text
        else: # Если через URL
            if len(params) > 0:
                req = ''
                for param in params:
                    if params[param] is not str: params[param] = str(params[param])
                    req += param +'='+ params[param] +'&'
                shttp += '?'+req       
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            r = http.request('GET', shttp)
            status = r.status
            if status == requests.codes.ok: d = r.data.decode('utf-8','ignore')
            
        if status != requests.codes.ok:
            return '#problem: ' + str(r.status_code)
        else:
            # Для тестирования
            with open('url.html','w', encoding='utf-8') as f:
                f.write(d)
            f.close()
            return d

    # Поиск значений в html (если ball то выводится список значений)
    def Find(data, sfind, sstart = '>', send = '<', ball = True):
        mtext = []
        start = 0; end = 0
        while start >= 0:
            start = data.find(sfind, start)
            if start > 0: # если есть признак
                start = data.find(sstart, start + 1)
                end = data.find(send, start + 1)
                ftext = data[start+len(sstart):end]
                if ball == False: return ftext
                mtext.append(ftext)
            else:
                return '#bug: none'
        return mtext

# здесь тестовая обработка #
stest = input('Введите тестовую фразу: ')
url = 'https://www.booking.com/searchresults.ru.html'
params = {'checkin_month':3,'checkin_monthday':8,'checkin_year':2018,
                  'checkout_month':3,'checkout_monthday':9,'checkout_year':2018,
                  'dest_type':'city','group_adults':1,'group_children':0,
                  'order':'price','raw_dest_type':'city','sb_price_type':'total'}
print(URL.GetURL(url,stext=stest,textparam='ss',params=params))

sdata = URL.GetData(url,stext=stest,textparam='ss',params=params)
if sdata[0]=='#':
    print(sdata)
else:
    print('Данные успешно записаны в файл Url.html!')

print(URL.Find(sdata, sfind='title=',sstart='"',send='"'))

import time; time.sleep(5)
