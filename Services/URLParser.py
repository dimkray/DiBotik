# -*- coding: utf-8 -*-
import Fixer
import requests
import certifi
import urllib3
import json
from urllib.parse import urlencode
from urllib.parse import quote
from bs4 import BeautifulSoup

def cln(text):
    m = []
    texts = text.split('\n')
    for i in texts:
        i = i.strip()
        if i != '':
            m.append(i)
    text = ''
    for i in m:
        text += i + '\n'
    return text[:-1]

class URL:
    # Возвращает URL
    def GetURL(shttp, stext = '', textparam = '', params = {}):
        try:
            stext = stext.replace(' ','+')
            stext = format(quote(stext))
            if len(params) > 0 or len(textparam) > 0:
                if len(textparam) > 0: params[textparam] = stext
            if len(params) > 0:
                req = ''; x = 0
                for param in params:
                    if params[param] is not str: params[param] = str(params[param])
                    if x != 0: req += '&'
                    req += param +'='+ params[param]
                    x += 1
                shttp += '?'+req             
            return shttp
        except Exception as e:
            Fixer.errlog('URL.GetURL', str(e))
            print('#bug: ' + str(e))

    # Открывает URL без параметров
    def OpenURL(url, bsave = False):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
            r = requests.get(url, headers = headers)
            # для тестирования
            if bsave:
                with open('URL.html', 'w', encoding='utf-8') as f:
                    f.write(r.text) #.decode('cp1251'))
            return r.text
        except Exception as e:
            Fixer.errlog('URL.OpenURL', str(e))
            return '#bug: ' + str(e)
        
    # Получение html/основного текста по запросу
    def GetData(shttp, stext = '', textparam = '', params = {}, headers = {},
                brequest = True, bsave = False, bjson = False, google = True):
        #try:
            if google == True: stext = stext.replace(' ','+')
            stext = format(quote(stext))
            if len(textparam) > 0: params[textparam] = stext
            else:
                if len(stext) > 0: shttp += format(quote(stext))
            status = 0; d = '' # Данные для ответа
            if brequest: # Если через request
                r = requests.get(shttp, params=params, headers=headers, verify=False)
                print(shttp)
                status = r.status_code
                if status == requests.codes.ok:
                    if bjson: d = r.json()
                    else: d = r.text
            else: # Если через URLlib
                if len(params) > 0:
                    req = ''; x = 0
                    for param in params:
                        if params[param] is not str: params[param] = str(params[param])
                        if x != 0: req += '&'
                        req += param +'='+ params[param]
                        x += 1
                    shttp += '?'+req       
                http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
                print(shttp)
                r = http.request('GET', shttp)
                status = r.status
                if status == requests.codes.ok:
                    d = r.data.decode('utf-8','ignore')
                    if bjson: d = json.loads(d)
                
            if status != requests.codes.ok:
                return '#problem: ' + str(status)
            else:
                if bsave:
                    # Для тестирования
                    with open('test.html','w', encoding='utf-8') as f:
                        f.write(d)
                    f.close()
                return d
##        except Exception as e:
##            Fixer.errlog('URL.GetData', str(e))
##            print('#bug: ' + str(e))               

class Parser: # Класс парсинга
    # Поиск значений в html (если ball то выводится список значений)
    def Find(data, sfind, sstart = '', send = '', ball = True):
        try:
            mtext = []
            start = 0; end = 0
            while start >= 0:
                start = data.find(sfind, start)
                if start > 0: # если есть признак
                    if sstart != '':
                        start = data.find(sstart, start + 1)
                    if send != '':
                        end = data.find(send, start + 1)
                    else: 
                        end = start + len(sfind)
                    ftext = data[start+len(sstart):end]
                    if ftext.find('<') >= 0: continue
                    if ball == False: return ftext
                    mtext.append(ftext)
                else:
                    if len(mtext) == 0: return '#bug: none'
            return mtext
        except Exception as e:
            Fixer.errlog('URL.Find', str(e))
            print('#bug: ' + str(e))   

    # Парсинг html
    def Parse(htmltext, sdiv='div', sclass='', stype='text'):
        Fixer.log('URL.Parse')
        results = []
        soup = BeautifulSoup(htmltext, 'lxml')
        if sclass == '': qlist = soup.find_all(sdiv)
        else: qlist = soup.find_all(sdiv, {'class': sclass})
        if len(qlist) > 0:
            for item in qlist:
                if stype == 'text':
                    results.append(cln(item.text))
                elif stype == 'href':
                    results.append(item.get('href'))
                else:
                    results.append(str(item))
            return results
        else: # нет
            results.append('#bug: none')
            return results
