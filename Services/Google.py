# -*- coding: utf-8 -*-

import config
import Fixer
import certifi
import urllib3
import requests
import json
from urllib.parse import urlencode
from urllib.parse import quote
from Services.URLParser import URL, Parser


# Чтение/парсинг сайта - получение основной информации
def ReadSite(url):
    print('Чтение: '+url)
    s = ''
    data = URL.GetData(url, brequest=False)
    if data[0] != '#':
        text = Parser.Find(data, '<p>', sstart='>', send='</p>', ball=True)
        if text[0] != '#':
            for ss in text:
                s += '\n' + ss
                if len(s) > 500:
                    s += '...'
                    break
            s += '\n' + url
    s = Fixer.strSpec(s)
    print('Результат: ' + s)
    return s      


class Google:
    # Сервис получения коротких гиперссылок
    def Shorten(url):
        try:
            req_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + config.GShort_Key
            payload = {'longUrl': url}
            headers = {'content-type': 'application/json'}
            r = requests.post(req_url, data=json.dumps(payload), headers=headers)
            if r.status_code == requests.codes.ok:      
                data = json.loads(r.text)
                rez = data['id']
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                rez = '#problem: '+ str(r.status_code)
            return rez
        except Exception as e:
            Fixer.errlog('Google.Shorten', str(e))
            return '#bug: ' + str(e)

    def Short(url):
        try:
            #http = 'https://www.googleapis.com/urlshortener/v1/url'
            #payload = {'key': config.GShort_Key, 'longUrl': url} 
            #r = requests.post(http, params=payload)
            post_url = 'https://www.googleapis.com/urlshortener/v1/url'
            payload = {'key': config.GShort_key, 'longUrl': url}
            headers = {'content-type': 'application/json'}
            r = requests.post(post_url, data=json.dumps(payload), headers=headers)
            #client = googl.Googl(config.GShort_Key)
            #r = client.shorten(url)
            if r.status_code == requests.codes.ok:      
                data = r.json()
                rez = data['id']
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                rez = '#problem: '+ str(r.status_code)
            return rez
        except Exception as e:
            Fixer.errlog('Google.Short', str(e))
            return '#bug: ' + str(e)

    # Сервис поиска толкования/определения слова или фразе
    def Define(text):
        try:
            text = text.strip()
            url = URL.GetURL('https://www.google.ru/search', stext='define '+text, textparam='q')
            Fixer.htext = url
            data = URL.OpenURL(url)
            mItems = ['#bug: none define']; tsend = ''
            if data[0] != '#':
                mItems = Parser.Parse(data, sdiv='div', sclass='PNlCoe', stype='text')
            if mItems[0][0] == '#': return 'Не удалось найти определение слову: ' + text
            if len(mItems) < 2: tsend = mItems[0]
            else:
                i = 0
                for item in mItems:
                    i += 1
                    if i > 7: continue # ограничение в 7 значений
                    tsend += '%i. %s\n' % (i, item)
            return tsend
        except Exception as e:
            Fixer.errlog('Google.Define', str(e))
            return '#bug: ' + str(e)

    # Сервис калькулятора
    def Calc(text):
        try:
            text = text.replace(' ', '')
            #text = text.replace('+','%2B')
            url = URL.GetURL('https://www.google.ru/search', stext=text, textparam='q')
            Fixer.htext = ''
            data = URL.OpenURL(url, bsave=True)
            if data[0] != '#':
                mItems = Parser.Parse(data, sdiv='span', sclass='cwcot', stype='text')
            if mItems[0][0] == '#': return 'Не удалось вычислить: ' + text
            tsend = mItems[0]
            return tsend
        except Exception as e:
            Fixer.errlog('Google.Calc', str(e))
            return '#bug: ' + str(e)

    # поиск формы xpdopen
    def xpdopen(text):
        m = Parser.Parse(text, sclass='xpdopen', stype='text')
        if len(m) > 0:
            print(m[0])
            return m[0]
        else:
            return ''

    # Сервис поиска универсальной карты (с маршрутами или обозначениями)
    def Search(text, bmap=False):
        try:
            data = URL.GetData('https://www.google.ru/search', stext=text, textparam='q', brequest=False, bsave=True)
            if data[0] != '#':
                # поиск карты
                if bmap:
                    ftext = Parser.Find(data, 'https://maps.google.ru/maps?q=', send='"', ball=False)
                    if ftext[0] != '#':
                        ftext = ftext.replace('%2B', '%20')
                        Fixer.htext = ftext #назначаем гиперссылку
                        #Fixer.htext = Google.Short(Fixer.htext) # делаем её короткой
                        # Поиск картинки
                        #start = d.find('/maps/vt/data')
                        #if start > 0: # признак картинки к карте
                        #    end = d.find('"',start)
                        #    ftext = 'https://www.google.ru' + d[start+5:end]
                        #    print(ftext)
                        #    return ftext
                        #else: # если картинки нет
                        return 'Я нашёл ответ! Открывай ниже ссылку!'
                    else:
                        print('#bug: none map')
                # поиск текста
                ftext = Parser.Find(data, 'href="/search?newwindow', sstart=':', send='+', ball=True)
                atext = Parser.Find(data, '<a href="/url?q=', sstart='q=', send='&', ball=True)
                s = ''
                if atext[0] != '#': s = ReadSite(atext[0])
                if s == '' and ftext[0] != '#':
                    i = 0
                    while s == '':
                        s = ReadSite(ftext[i])
                        i += 1
                        if i >= len(ftext): break
                if ftext[0] != '#':
                    i = 1; sl = ''
                    for ss in ftext:
                        i += 1
                        if i > 0: sl += '\n' + ss # '\n' + atext[i-1] + '\n' + ss
                        if i > 8: break
                    Fixer.htext = sl #назначаем гиперссылку
                if s != '': return s
                else:
                    print('#bug: none')
                    return '#bug: none'
            else:
                return data
        except Exception as e:
            Fixer.errlog('Google.Search', str(e))
            return '#bug: ' + str(e)            
