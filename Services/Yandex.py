# -*- coding: utf-8 -*-
import requests
import json
# import logging
import config
import Fixer
from Services.Geo import Geo
from DB.SQLite import SQL
from Profiler import decorator

tformat = '%Y-%m-%d %H:%M:%S'
path = 'rasp-yandex.json'

dir_lang = []
for item in Fixer.yaDirLang:
    dir_lang.append(item[0]+'-'+item[1])

tr_type = [['САМОЛ', 'plane', 3], ['ПОЕЗД', 'train', 1], ['ЭЛЕКТР', 'suburban', 1],
           ['АВТОБУС', 'bus', 2], ['ВОДН', 'water', 4], ['ВЕРТОЛ', 'helicopter', 3]]
trd = {'All': 'любой транспорт', 'plane': 'самолёт', 'train': 'поезд', 'suburban': 'электричка',
       'bus': 'автобус', 'water': 'водный транспорт', 'helicopter': 'вертолёт'}
mounth = ['ЯНВАРЯ', 'ФЕВРАЛЯ', 'МАРТА', 'АПРЕЛЯ', 'МАЯ', 'ИЮНЯ', 'ИЮЛЯ',
          'АВГУСТА', 'СЕНТЯБРЯ', 'ОКТЯБРЯ', 'НОЯБРЯ', 'ДЕКАБРЯ']
trSt = {'': 0, 'unknown': 0, 'train_station': 1, 'platform': 1, 'station': 1,
        'bus_station': 2, 'bus_stop': 2, 'airport': 3, 'whafr': 4, 'river_port': 4, 'port': 4}


# Поиск идентификатора языка

def FindLang(slang):
    slang = slang.strip()
    if slang.upper() in Fixer.yaLangs:
        return Fixer.yaLangs[slang.upper()]
    else:
        return ''


# Функция - есть ли станция/город в базе
def isStation(station):
    if len(SQL.ReadRowLike('stations', 'nameU', station.upper())) > 0:
        return True
    else:
        return False


# Функция - есть ли станция/город в базе (с фиксацией региона)
def isStational(station):
    iSt = 0
    row = SQL.ReadRowLike('stations', 'nameU', station.upper())
    if len(row) > 0:
        iSt += 1
        if Fixer.region == '':
            if row[2] != '':
                Fixer.region = row[2]
            elif row[3] != '':
                Fixer.region = row[3]
            elif row[4] != '':
                Fixer.region = row[4]
    return True if iSt > 0 else False


# Функция вариантов станции/города в базе
def eStation(stat):
    if isStational('Г. ' + stat + ' '): 
        return 'Г. ' + stat + ' '
    if isStation('Г. ' + stat + ' '): 
        return 'Г. ' + stat + ' '
    if isStation(stat + ' '): 
        return stat + ' '
    if isStation(stat):
        return stat
    return ''


# Функция поиска станции/города в базе
def FindStation(station):
    db2 = []; st = []
    sstation = ''
    istation = ''
    db1 = SQL.ReadRows('stations', 'nameU', station.upper())
    db1 += SQL.ReadRowsLike('stations', 'nameU', station.upper())
    print('Анализ станции/города: ' + station)
    x = 0
    for ist in db1:
        print(str(x) +' - '+ ist[1] + ' ' + ist[2] + ' ' + ist[3] + ' ' + ist[4] + ' ' + ist[5] )
        x += 1
        if x >= 100:
            print('...')
            break
    if x < 1:
        print('В базе данных не найдены соотвествия :(')
    elif x == 1:
        print('Станция назначена автоматически!')
        istation = db1[0][8]
        Fixer.nameSt = db1[0][1]
        Fixer.LastCoords.append(Fixer.Coords)
        Fixer.Coords = []
        Fixer.Coords.append(db1[0][7])
        Fixer.Coords.append(db1[0][6])
    else:
        print('Регион поиска: ' + Fixer.region)
        for wordz in db1:
            bApp = False
            if Fixer.region != '':
                if Fixer.region.upper() in wordz[10] or Fixer.region.upper() in wordz[11] or Fixer.region.upper() in wordz[12]:
                    db2.append(wordz); bApp = True
            if Fixer.iTr > 0 and trSt[wordz[5]] > 0 and bApp == False:
                if Fixer.iTr == trSt[wordz[5]]:
                    db2.append(wordz)
        if len(db2) > 0:
            print('Фильтрация...')
            x = 0
            for ist in db2:
                print(str(x) + ' - ' + ist[1] + ' ' + ist[2] + ' ' + ist[3] + ' ' + ist[4] + ' ' + ist[5])
                x += 1
            st = db2[1]
        else:
            for wordz in db1:
                if wordz[9][1:3] == 'Г.':
                    st = wordz
                    break
            if sstation == '':
                st = db1[1]
        if Fixer.region == '':
            Fixer.region = st[2]
        if Fixer.region == '':
            Fixer.region = st[3]
        if Fixer.region == '':
            Fixer.region = st[4]
        print('Назначена станция: ' + st[1] + '\n')
        istation = st[8]
        Fixer.nameSt = st[1]
        Fixer.LastCoords.append(Fixer.Coords)		
        Fixer.Coords = []
        Fixer.Coords.append(st[7])
        Fixer.Coords.append(st[6])
    return istation

class Ya:
    
    # Сервис Яндекс.Расписание
    # Сервис с актуальными расписаниями самолётов, поездов, электричек, автобусов, теплоходов и паромов
    # https://tech.yandex.ru/rasp/

    ##### ОСНОВНОЙ КОД #####

    @decorator.benchmark
    def FindRasp(s):
        try:
            rez = '#bug: Ya.Rasp'
            Fixer.iTr = 0
            Fixer.region = ''; Fixer.nameSt = ''
            stime = ''; bnow = True
            st1 = ''; st2 = ''
            from datetime import date, datetime, timedelta

            words = s.strip().split(' ')
            sdate = str(date.today());
            stype = 'All'; x = 0
            for word in words:
                x += 1
                isCon = False
                Uw = word.upper()
                Uw = Uw.replace('Ё','Е')
                Uw = Uw.replace('_',' ')
                # если указан регион поиска
                if Uw[0] == '(':
                    Fixer.region = Uw[1:-1]
                    continue
                # временные параметры
                if Uw == 'СЕЙЧАС':
                    bnow = True
                    sdate = str(date.today()); continue
                if Uw == 'СЕГОДНЯ':
                    bnow = False
                    sdate = str(date.today()); continue
                if Uw == 'ЗАВТРА':
                    bnow = False
                    sdate = str(date.today() + timedelta(days=1)); continue
                if Uw == 'ПОСЛЕЗАВТРА':
                    bnow = False
                    sdate = str(date.today() + timedelta(days=2)); continue
                if Uw == 'ВЧЕРА':
                    bnow = False
                    sdate = str(date.today() - timedelta(days=1)); continue
                if Uw.count('-')>1 or Uw.count('.')>1 or Uw.count('/')>1:
                    bnow = False
                    sdate = Uw 
                    sdate = sdate.replace('.','-')
                    sdate = sdate.replace('/','-')
                    Fixer.trDate = sdate
                    continue
                if Uw.isdigit():
                    m = 0
                    for mou in mounth: 
                        if mou in words[x].upper() and words[x].upper().find(mou) == 0:
                            bnow = False
                            if m < 9:
                                sdate = '2018-0'+ str(m+1) + '-' + Uw
                            else:
                                sdate = '2018-'+ str(m+1) + '-' + Uw
                            isCon = True
                            continue
                        m += 1

                # ключевые признаки
                if Uw == '-' or Uw == '->' or Uw == 'В' or Uw == 'ДО':
                    st1 = eStation(words[x-2].upper())
                    st2 = eStation(words[x].upper())
                    continue
                if Uw == 'ИЗ' or Uw == 'ОТ':
                    st1 = eStation(words[x-2].upper())
                    continue
                if Uw == '<-':
                    st1 = eStation(words[x].upper())
                    st2 = eStation(words[x-2].upper())
                    continue
                for wordz in tr_type: # тип транспорного средства
                    if wordz[0] in Uw: 
                        stype = wordz[1]
                        Fixer.iTr = wordz[2]
                        isCon = True
                        continue
                if isCon:
                    continue
                # Проверяем не город/станция ли это
                if len(Uw) < 4:
                    continue
                if len(st1) > 0 and len(st2) > 0:
                    continue
                if st1 == '':
                    st1 = eStation(Uw)
                    continue
                if st2 == '':
                    st2 = eStation(Uw)
                    continue
            print('Город 1: ' + st1 + ' Город 2:' + st2)
            # Поиск города/станции в базе и сохранение
            if st1 != '' and st2 != '':
                st1 = FindStation(st1)
                Fixer.St1 = Fixer.nameSt
                st2 = FindStation(st2)
                Fixer.St2 = Fixer.nameSt
            else:
                rez = 'В запросе не указана начальная и/или конечная станция/город.\n'
                if st1 != '' or st2 != '':
                    rez += 'Найдена станция/город: '+st1+st2
                return rez
            
            if bnow == True:
                stime = str(datetime.today())

            http = 'https://api.rasp.yandex.net/v3.0/search/'
            payload = {'from': st1, 'to': st2, 'format': 'json', 
                            'lang': 'ru_RU', 
                            'apikey': config.YaRasp_key, 
                            'date': sdate,
                            'transport_types': stype,
                            'limit': '100'} 
            if stype == 'All': del payload['transport_types']

            r = requests.get(http, params=payload)

            sAdd = ' - OK\n' if r.status_code == requests.codes.ok else ' - have a problem'
            if r.status_code != requests.codes.ok:
                return '#problem: ' + str(r.status_code)

            if r.status_code == requests.codes.ok:
                data = r.json()
                # сохранение ответа в файл
                with open('rasp.json', 'w') as f:
                    json.dump(r.json(), f)
                f.close()
                print('Найдено рейсов: ' + str(data['pagination']['total']))
                rez = '%' + str(data['pagination']['total']) + ' Расписание: ' + trd[stype] + ' на дату ' + sdate + ':\n'
                for i in data['segments']:
                    t1 = i['departure']
                    t1 = t1[t1.find('T') + 1:t1.find('+')]
                    etime = datetime.strptime(sdate+' '+t1,tformat)
                    now = datetime.utcnow() + timedelta(hours=Fixer.TimeZone)
                    if stime == '' or now < etime:
                        t1 = t1[:-3]
                        t2 = i['arrival']
                        t2 = t2[t2.find('T') + 1:t2.find('+')]
                        t2 = t2[:-3]
                        no = i['thread']['number'] + ': '
                        title = i['thread']['title'] + ' '
                        dur = str(int((i['duration']%3600)/60)) + ' мин. '
                        if i['duration']//3600>0:
                            dur = str(int(i['duration']//3600)) + ' ч. ' + dur
                        tt = i['thread']['transport_type']
                        prc = ''
                        try:
                            minPrc = 10000000
                            maxPrc = 0
                            for j in i['tickets_info']['places']:
                                if j['price']['whole'] < minPrc: minPrc = j['price']['whole']
                                if j['price']['whole'] > maxPrc: maxPrc = j['price']['whole']
                                if minPrc == maxPrc:
                                    prc = str(maxPrc) +' '+ j['currency']
                                else:
                                    prc = str(minPrc) +'-'+ str(maxPrc) +' '+ j['currency']
                        except:
                            prc = ''            
                        sR = t1 + ' - ' + t2 + ' : ' + trd[tt] + ' ' + no + title + ' : ' + dur + prc + '\n'
                        rez += sR
                        # Добавляем гиперссылку
                rez += '#https://rasp.yandex.ru/search/?fromId='+st1+'&toId='+st2+'&when='+sdate
            return rez
        except Exception as e:
            Fixer.errlog('Ya.FindRasp', str(e))
            return '#bug: ' + str(e)
    
    # Сервис Яндекс.Спеллер
    # Яндекс.Спеллер помогает находить и исправлять орфографические ошибки
    # в русском, украинском или английском тексте. Языковые модели Спеллера
    # включают сотни миллионов слов и словосочетаний.
    # https://tech.yandex.ru/speller/doc/dg/reference/checkText-docpage/
    @decorator.benchmark
    def Speller(s):
        try:
            rez = '#bug: Ya.Speller'
            http = 'https://speller.yandex.net/services/spellservice.json/checkText'
            payload = {'text': s, 'options': 4} 
            r = requests.get(http, params=payload)
            if r.status_code == requests.codes.ok:      
                data = r.json()
                rez = ''; x = 0
                for word in data:
                    if word['code'] == 2: # Повтор слова
                        rez += s[x:word['pos']] # вырезаем слово
                        x = word['pos'] + word['len']
                    if word['code'] == 1 or word['code'] == 3: # Неверное употребление прописных и строчных букв
                        if word['s']:
                            rez += s[x:word['pos']] + word['s'][0] # заменяем слово
                            x = word['pos'] + word['len']  
                rez += s[x:]
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                rez = '#problem: '+ str(r.status_code)
            return rez
        except Exception as e:
            Fixer.errlog('Ya.Speller', str(e))
            return '#bug: ' + str(e)

    # Сервис Яндекс.Переводчик
    @decorator.benchmark
    def Translate(s, lang1, lang2):
        try:
            rez = ''
            #автоопределение языка
            if lang1 == 'авто':
                http = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
                payload = {'key': config.YaTranc_key, 'text': s, 'hint': 'ru,en,fr,it,de'}
                r = requests.get(http, params=payload)
                if r.status_code == requests.codes.ok:      
                    data = r.json()
                    if data['lang']: lang1 = data['lang']
                else:
                    # Если ошибка - то спец.сообщение с номером ошибки
                    return '#problem: '+ str(r.status_code)
                lang2 = FindLang(lang2)
            else:
                lang1 = FindLang(lang1)
                lang2 = FindLang(lang2)
            dir_tr = lang1 + '-' + lang2
            http = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
            payload = {'key': config.YaTranc_key,
                        'text': s, 'lang': dir_tr, 'options': 1} 
            r = requests.get(http, params=payload)
            if r.status_code == requests.codes.ok:      
                data = r.json()
                rez = data['text'][0]
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                rez = '#problem: '+ str(r.status_code)
            return rez
        except Exception as e:
            Fixer.errlog('Ya.Translate', str(e))
            return '#bug: ' + str(e)

    # Сервис Яндекс поиск объектов/организаций
    @decorator.benchmark
    def Objects(text, Xloc=Fixer.X, Yloc=Fixer.Y, dr=10, fix=1):
        try:
            rez = ''
            if Xloc == Yloc == 0: # если координаты не заданы
                Xloc = 37.619955
                Yloc = 55.753767
                rez = 'Не определены координаты старта поиска. Ищу ближайшие объекты от мавзалея :)\nЧтобы поиск можно было осуществлять от текущего местоположения, необходимо включить геолокацию (кнопочка в меню).'
            dxy = dr/55 # преобразование км в угловые расстояния
            http = 'https://search-maps.yandex.ru/v1/'
            payload = { 'apikey': config.YaObj_key,
                        'text': text,
                        'lang': 'ru_RU',
                        'll': str(Xloc) + ',' + str(Yloc), #координаты центра поиска - по умолчанию Геолокация
                        'spn': str(dxy) + ',' + str(dxy), #размер области поиска (протяжённость по долготе и широте)
                        'rspn': fix, #Признак «жесткого» ограничения области поиска, 1 - ограничить поиск
                        'results': 500}                
            r = requests.get(http, params=payload)
            print(payload)
            if r.status_code == requests.codes.ok:      
                Fixer.Obj = []
                data = r.json()
                #print(data)
                for ft in data['features']:
                    if 'CompanyMetaData' in ft['properties']: # Если это организация
                        address = ''; url = ''; cats = ''; tels = ''; hours = ''
                        if 'address' in ft['properties']['CompanyMetaData']:
                            address = ft['properties']['CompanyMetaData']['address']
                        if 'Categories' in ft['properties']['CompanyMetaData']:
                            for cat in ft['properties']['CompanyMetaData']['Categories']:
                                cats += cat['name'] + ', '
                        if 'Phones' in ft['properties']['CompanyMetaData']:
                            for tel in ft['properties']['CompanyMetaData']['Phones']:
                                tels += tel['formatted'] + ', '
                        if 'Hours' in ft['properties']['CompanyMetaData']:
                            hours = ft['properties']['CompanyMetaData']['Hours']['text']
                        if 'url' in ft['properties']['CompanyMetaData']:
                            url = ft['properties']['CompanyMetaData']['url']
                        aft = [True, ft['properties']['CompanyMetaData']['name'],  # название организации
                               address, # полный адрес
                               cats, hours, tels, url,
                               ft['geometry']['coordinates'][0], # Координата X
                               ft['geometry']['coordinates'][1]] # Координата Y
                    else:
                        aft = [False, # признак географического объекта
                               ft['properties']['name'], # Название объекта
                               ft['properties']['GeocoderMetaData']['text'], # Полное название (географический адрес)
                               '','','','',
                               ft['geometry']['coordinates'][0], # Координата X
                               ft['geometry']['coordinates'][1]] # Координата Y
                    Fixer.Obj.append(aft)                
            else:
                return '#problem: ' + str(r.status_code)

            # Обработка результатов поиска
            gObj = 0; oObj = 0
            for i in Fixer.Obj:
                if i[0]: oObj +=1 # число организаций
                else: gObj +=1 # число геогр. объектов				
            sorg = ''; sobj = ''; sand = ''
            if oObj > 0: sorg = str(oObj) + ' организаций/ию'
            if oObj > 499: sorg = 'более ' + str(oObj) + ' организаций'
            if gObj > 0: sobj = str(gObj) + ' географических/ий объект/ов'
            if oObj != 0 and gObj != 0: sand = ' и '
            if oObj == 0 and gObj == 0:
                rez = 'Не нашёл ни одного объекта с названием "'+text+'" в радиусе '+str(dr)+'км :(\nМожет надо указать другие параметры поиска? Либо задать больший радуис поиска, указав дополнительно ...в пределах 500 км, например.'
            #print(oObj)
            #print(gObj)
            rez = 'Нашёл ' + sorg + sand + sobj + ' в радиусе '+ str(dr) + ' км.\n'
            #print(Fixer.Obj)
            if oObj + gObj > 5: rez += 'Из них будут показаны 5 ближайших:'
            srez = []; dis = 0; stext = ''
            for i in Fixer.Obj:
                if i[0]:
                    stext = 'Организация: '+i[1]+'\nАдрес: '+i[2]+'\nGPS-координаты: '+str(i[8])+','+str(i[7]) + '\n'
                    stext += 'Категории: '+i[3]+'\nЧасы работы: '+i[4]+'\nТелефоны: '+i[5]+'\nURL: '+i[6]
                else: # геогр. объект
                    stext = 'Объект: '+i[1]+'Расположение: '+i[2]+'\nGPS-координаты: '+str(i[8])+','+str(i[7])
                dis = Geo.Distance(Xloc, Yloc, i[7], i[8])
                drez = [dis, stext]
                srez.append(drez)
            srez.sort()
            Fixer.sObj = srez
            x = 1
            for i in srez:
                if x > 5: break
                rez += '\n['+str(x)+'] '+ i[1] + '\n'
                if i[0] > 1:
                    dis = 10 * i[0]
                    dis = int(dis) / 10
                    rez += '  Расстояние до объекта: ' + str(dis) + ' км.'
                else:
                    dis = 100 * i[0]
                    dis = int(dis) * 10
                    rez += '  Расстояние до объекта: ' + str(dis) + ' м.'
                x += 1
            return rez
        except Exception as e:
            Fixer.errlog('Ya.Objects', str(e))
            return '#bug: ' + str(e)

    # Сервис Яндекс.Координаты
    # Яндекс.Координаты возвращает географические координаты города/станции
    @decorator.benchmark
    def Coordinates(station):
        try:
            s = eStation(station.upper())
            print(s)
            if s == '': return '#problem: не найдено ни одного объекта'
            s = FindStation(s)
            if s == '': return '#problem: не найдено ни одного объекта'
            if Fixer.Coords[0] == Fixer.Coords[1] == 0: return '#poblem: не заданы координаты'
            return str(Fixer.Coords[1]) + ', ' + str(Fixer.Coords[0])
        except Exception as e:
            Fixer.errlog('Ya.Coordinates', str(e))
            return '#bug: ' + str(e)

    # Сервис Яндекс.Каталог
    # Яндекс.Каталог возвращает информацию о сайте (тиц, раздел, регион)
    @decorator.benchmark
    def Catalog(url):
        try:
            url = url.strip()
            if len(url) > 2:
                mfind = SQL.ReadRowsLike('yaCatalog', 'site', url)
                icount = len(mfind)
                s = 'Найдено совпадений: ' + str(icount)
                if icount == 0: return 'Сайт или часть сайта "%s" не найдена :(\nСледует уточнить строку поиска или убедиться, что сайт существует.' % url
                if icount > 5: s += '. Но будут показаны первые 5:'; icount = 5
                else: s += ':'
                try:
                    mfind = sorted(mfind, key=lambda st: st[3], reverse=True)
                except: pass
                for i in range(0,icount):
                    s +='\n[%i] %s - %s (ТИЦ: %s)' % (i+1, mfind[i][1], mfind[i][2], mfind[i][3])
                    s +='\nРаздел: %s' % mfind[i][4]
                    for j in range (5, 10):
                        if mfind[i][j].strip() != '':
                            s +=' -> ' + mfind[i][j]
                    s +='\nРегион: %s' % mfind[i][9]
                    for j in range (11, 14):
                        if mfind[i][j].strip() != '':
                            s +=' -> ' + mfind[i][j]
                return s
            else: return 'Строка "%s" для поиска информации по сайту слишком мала!' % url
        except Exception as e:
            Fixer.errlog('Ya.Catalog', str(e))
            return '#bug: ' + str(e)
        
    # Сервис Яндекс.Каталог
    # Яндекс.Каталог ищет сайт по запросу
    @decorator.benchmark
    def FindCatalog(text):
        try:
            text = text.upper().strip()
            if len(text) > 2:
                mfind = []
                for col in ['site','section','section2','section3','section4',
                      'section5','section6','region','region2','region3','region4',
                      'titleU','regionRuU']:
                    mfind += SQL.ReadRowsLike('yaCatalog', col, text)
                icount = len(mfind)    
                s = 'Найдено совпадений: ' + str(icount)
                if icount == 0: return 'Сайт по поисковой строке "%s" не найден :(' % text
                if icount > 5: s += '. Но будут показаны первые 5:'; icount = 5
                else: s += ':'
                print(icount)
                try:
                    mfind = sorted(mfind, key=lambda st: st[3], reverse=True)
                except: pass
                for i in range(0,icount):
                    s +='\n[%i] %s - %s (ТИЦ: %s)' % (i+1, mfind[i][1], mfind[i][2], mfind[i][3])
                    s +='\nРаздел: %s' % mfind[i][4]
                    for j in range (5,10):
                        if mfind[i][j].strip() != '':
                            s +=' -> ' + mfind[i][j]
                    s +='\nРегион: %s' % mfind[i][10]
                    for j in range (11,14):
                        if mfind[i][j].strip() != '':
                            s +=' -> ' + mfind[i][j]
                return s
            else: return 'Строка "%s" для поиска сайта слишком мала!' % text
        except Exception as e:
            Fixer.errlog('Ya.FindCatalog', str(e))
            return '#bug: ' + str(e)

