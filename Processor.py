# -*- coding: utf-8 -*-
# Процессор - обработчик основных сервисов

import config
import Fixer
import Bot
import apiai
import json
import random
import DefProcess

from Services.Fun import Fun
from Services.Yandex import Ya
from Services.Google import Google
from Services.Wikipedia import Wiki
from Services.User import User
from Services.Rates import Rate
from Services.Weather import Weather
from Services.Geo import Geo
from Services.House import Booking
from Services.RSS import RSS
from Services.IATA import IATA
from Services.StrMorph import String, Word
from Services.DaData import strData
from Chats.Chats import Chat
from DB.SQLite import SQL

# получение переменных в массив [] из строки переменных для сервиса
def getparams(text, separator='|'):
    if text.find(separator) < 0 and separator != ';' : # нет текущего сепаратора
        if text.find(' - ') > 0: separator = ' - '
        else:
            if text.find(',') > 0: separator = ','
            else: separator = ' '
    if text.find('[R') >= 0: # Признак радиуса интереса
        poz = text.find('[R')
        end = text.find(']',poz)
        print(text[poz+2,end-1])
        Fixer.Radius = float(text[poz+2,end-1])
        text = text.replace('[R'+text[poz+2,end-1]+']','') # Убираем радуис интереса
    m = text.split(separator)
    x = 0
    for im in m:
        m[x] = im.strip(); # убираем лишние пробелы
        x += 1
    #print(m)
    return m

# Работа с сервисами
# ---------------------------------------------------------
# сервис AI : #ai: всякий бред
def ai(text):
    Fixer.log('Processor.AI', 'Запуск AI')
    try:
        request = apiai.ApiAI(config.apiAI_key).text_request()
        request.lang = 'ru' # На каком языке будет послан запрос
        request.session_id = str(Fixer.UserID) #'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
        # Запуск сервиса Google Dialogflow для обработки пользовательского запроса (ИИ)
        request.query = text # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        return responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    except Exception as e:
        Fixer.errlog(Fixer.Process, str(e))
        return '#bug: ' + str(e)

# ---------------------------------------------------------
# сервис Task : #task: type | time | times | Notice/Service
def task(text):
    Fixer.log('Task', text)
    import Notification
    from datetime import date, datetime, timedelta
    tformat = '%Y-%m-%d %H:%M:%S'
    Notification.Tasks = Fixer.LoadB('Tasks')
    params = getparams(text)
    params[0] = params[0].lower()
    if len(params) < 2: params.append(datetime.today().strftime('%H:%M:%S')) # params[1]
    if len(params) < 3: params.append('2') # params[2]
    if len(params) < 4: params.append('NULL') # params[3]
    s = '';
    delta = timedelta(days=1) # дельта по умолчанию - сутки
    if params[0] == 'alarm':
        s = 'Будильник успешно установлен!'
    elif params[0] == 'alarmlater':
        s = 'Отложенное уведомление успешно установлено!'
    elif params[0] == 'rss':
        s = 'Подписка на RSS-канал успешно активирована!'
        delta = timedelta(minutes=1)
    elif params[0] == 'del':
        Fixer.SaveB({}, 'Tasks')
        s = 'Все задания успешно удалены!'
        return s
    elif params[0] == 'all': # показать все задания
        s = 'Список заданий:'
        i = 0
        for itask in Notification.Tasks:
            s += '\n[%i] %s' % ( i, str(itask) )
            i += 1
        if i == 0: s += '\n( список пуст )'
        else: s += '\n\nМожно удалить все задания командой "task-del: all"'
        return s
    else:
        s = 'Неизвестная задача "%s"!' % params[0]
        return s
    m = [] # наполняем массив
    smsg = params[0] +'-'+ str(random.randint(100000, 999999)) # key
    skey = str(Fixer.ChatID) +':'+ smsg
    etime = datetime.strptime(str(date.today())+' '+params[1],tformat) + timedelta(hours=Fixer.TimeZone)
    if etime < datetime.today():
        etime = etime + timedelta(days=1)
    s += '\nНазвание: '+smsg+'\nСообщение\\сервис: '+params[3]+'\nВремя срабатывания: '+str(etime + timedelta(hours=Fixer.TimeZone))+'\nКоличество повторений: '+params[2]
    m.append(Fixer.bNotice) # 0 - вкл/выкл уведомление пользователя
    m.append(etime) # 1 - дата-время срабатывания задачи
    m.append(delta) # 2 - дельта следующего срабатывания / по умолчанию 1 день для alarm
    m.append(int(params[2])) # 3 - количество раз срабатывания (при 0/-1 бесконечный цикл)	
    scode = params[3]
    if params[3].upper() == 'NULL': 
        params[3] = smsg+'\nТы просил меня отправить сообщение в '+str(etime)
        scode = ''
    m.append(params[3]) # 4 - сообщение при уведомлении
    m.append(scode) # 5 - запускаемый сервис	
    Notification.Tasks[skey] = m
    #print(m)
    Fixer.SaveB(Notification.Tasks, 'Tasks') # Сохранение задач
    Fixer.log('Processor.Task', s)
    return s
	
# ---------------------------------------------------------
# сервис Answer : #answer: ответ
def answer(text):
    Fixer.log('Answer')
    if text == 'yes':
        Bot.SendMessage('Отлично!')
        if Fixer.Thema == 'Знакомство':
            Fixer.Service == 'acquaintance'
            tsend = User.Acquaintance()
    elif text == 'no':
        tsend = 'Хорошо. Значит в другой раз.\nГотов помочь, чем смогу!'
        Fixer.Thema == ''
        Fixer.Service == ''
    Fixer.log('Answer', tsend)
    return tsend

# ---------------------------------------------------------
# сервис Name - #name: имя
def name(text):
    text = text.strip()
    Fixer.log('Name')
    s = ''
    rName = SQL.ReadRow('names', 'nameU', text.upper().replace('Ё','Е'))
    if len(rName) > 0: # если найдено имя
        s = text + ': '
        if rName[1] == 1: # мужчина
            s += 'мужское имя'
        else:
            s += 'женское имя'
        s += '\nколичество не менее: ' + str(rName[2])
        s += '\nстрана распространения: ' + rName[3]
    else: # если не найдено имя
        s = 'Не удалось проанализировать имя '+text+' :('
    Fixer.log('Name', s)
    Fixer.Service == ''
    return s

# ---------------------------------------------------------
# сервис User - #user-<param>: значение
def user(param, text):
    Fixer.log('User')
    tsend = User.Info(param, text)
    Fixer.log('User', tsend)
    Fixer.Service == ''
    return tsend

# ---------------------------------------------------------
# сервис Acquaintance - #acquaintance:
def acquaintance():
    Fixer.log('Acquaintance')
    tsend = User.Acquaintance()
    Fixer.log('Acquaintance', tsend)
    return tsend

# ---------------------------------------------------------
# сервиса Fixer (информация) #fixer: <Параметр>
def fixer(text):
    Fixer.log('Fixer')
    text += ' '
    s = text[:text.find(' ')]
    s = s.upper()
    Fixer.Service == ''
    if s == 'XY': return str(Fixer.Y)+','+str(Fixer.X)
    elif s == 'NAME': return Fixer.Name
    elif s == 'AGE': return str(Fixer.Age)
    elif s == 'FIXER': return str(Chat.Save())
    elif s == 'ADDRESS': return Fixer.Address
    elif s == 'LASTLANG1': return str(Fixer.LastLang1)
    elif s == 'LASTLANG2': return str(Fixer.LastLang2)
    elif s == 'LASTSERVICE': return str(Fixer.LastService)
    elif s == 'LASTST1': return str(Fixer.LastSt1)
    elif s == 'LASTST2': return str(Fixer.LastSt2)
    else:
        Fixer.errProcess = Fixer.Process
        return '#err: неизвестный параметр: ' + s

# ---------------------------------------------------------
# Обработка результатов сервиса Яндекс.Расписание
def FormRasp(s):
    Fixer.log('FormRasp')
    tstr = s
    if s[0] == '%': # Рейсы найдены!
        nstr = s.find(' ',1)
        num = int(s[1:nstr]) # количество рейсов
        gstr = s.find('#',1)
        Fixer.htext = s[gstr+1:]
        routes = s[nstr+1:gstr-2].strip().split('\n')
        if num == 0:
            tstr = 'Печалька. Не нашёл ни одного прямого рейса :(\nМожет я не правильно тебя понял? Попробуй по другому сделать запрос!'
        elif 0 < num < 11:
            tstr = 'Нашёл ' + str(num) + ' рейс(ов)!\n'
        elif 10 < num < 300:
            tstr = 'Нашёл ' + str(num) + ' рейс(ов). Покажу первые 10.\n'
        elif 300 < num < 1000:
            tstr = 'Нашёл дохрена рейсов! ' + str(num) + '! Покажу первые 10.\n'
            tstr += s[num+1:gstr]
        else:
            tstr = 'Нашёл какое-то невероятное число рейсов! ' + str(num) + '! Может я где-то ошибся? Лучше зайди по ссылке, посмотри всё ли правильно.\n'
        if num > 0:
            x = 0
            for rout in routes:
                tstr += routes[x] + '\n'
                x += 1
                if x > 11: break
        if len(routes)-1 != num: # части рейсов нет
            tstr += '\n' + str(num-len(routes)-1) + 'рейс\рейсов на сегодня уже нет.'
        if len(routes)-1 == 0 and num > 0: # если уже рейсов нет
            tstr = 'На сегодня уже нет ни одного прямого рейса :('
    return tstr

# ---------------------------------------------------------
# сервис Booking : #booking: $geo-city | $checkin | $checkout | $people | $order | $dormitory
def booking(text, send=False):
    Fixer.log('Booking.com')
    from datetime import date
    tformat = '%Y-%m-%d'
    if send: Bot.SendMessage('Секундочку! Ищу подходящее жильё в сервисе Booking.com...')
    params = getparams(text)
    bDorm = True
    if len(params) < 2: params.append('Now')
    if len(params) < 3: params.append('Next')
    if len(params) < 4: params.append('1')
    if len(params) < 5: params.append('price')
    if len(params) < 6: params.append('1')
    if params[1].upper() == 'NOW': date.today().isoformat()
    if params[2].upper() == 'NEXT': str(date.strpdate(params[1],tformat) + 1)
    if params[5] != '1': bDorm = False
    
    mList = Booking.List(params[0], params[1], params[2], people=float(params[3]), order=params[4], dorm=bDorm)
    if mList[0] == '#': return mList
    tsend = 'Найдены следующие варианты:'
    x = 0
    for item in mList:
        x += 1
        if x > 7: continue # только 7 вариантов
        tsend += '\n' + item
    Fixer.log('Booking.com', tsend)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Расписание
def timetable(text, send=False):
    Fixer.log('TimeTable')
    if send: Bot.SendMessage('Секундочку! Ищу расписание транспорта в сервисе Яндекс.Расписания...')
    tsend = Ya.FindRasp(text)
    Fixer.log('Ya.Rasp', tsend)
    tsend = FormRasp(tsend)
    Fixer.log('FormRasp', tsend)
    if tsend[0] != '#':
        Fixer.LastSt1.append(Fixer.St1)
        Fixer.LastSt2.append(Fixer.St2)
        Fixer.LastTr.append(Fixer.iTr)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Переводчик
def translate(text):
    Fixer.log('Translate')
    if Fixer.Context:
        lang1 = Fixer.Lang1
        lang2 = Fixer.Lang2
    else:
        n1 = text.find(' - ')
        n2 = text.find(': ')
        if n1 > n2 or n1 < 1:
            lang1 = 'авто'
            lang2 = text[:n2]
        else:
            lang1 = text[:n1]
            lang2 = text[n1+3:n2]
    if lang1 == lang2: lang2 = 'английский'
    if lang1 == '$lang-from':
        lang1 = Fixer.Lang1
    else:
        Fixer.Lang1 = lang1
    if lang2 == '$lang-to':
        lang2 = Fixer.Lang2
    else:
        Fixer.Lang2 = lang2
    ttext = text[n2+2:]
    Fixer.log('Translate', ttext + ' | ' + lang1 + ' | ' + lang2)
    tsend = Ya.Translate(ttext, lang1, lang2)
    Fixer.log('Ya.Translate', tsend)
    if tsend[0] != '#':
        Fixer.LastLang1.append(Fixer.Lang1)
        Fixer.LastLang2.append(Fixer.Lang2)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс поиск объектов : #object: objName | Radius
def yaobject(text):
    Fixer.log('Ya.Object', text)
    param = getparams(text)
    ttext = param[0]
    rad = Fixer.Radius
    if len(param) > 1: rad = param[1]
    try:
        drad = int(rad)
    except:
        if rad == 'near': drad = 2
        else: drad = 100
    tsend = Ya.Objects(ttext, Xloc=Fixer.X, Yloc=Fixer.Y, dr=drad)
    Fixer.log('Ya.Object', tsend)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Координаты : #coordinates: $geo-city
def coordinates(text):
    Fixer.log('Ya.Координаты')
    if text == '': text = 'LOCATION'
    tsend = Ya.Coordinates(text)
    Fixer.log('Ya.Координаты', tsend)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Каталог : #site: type(info/find) - $site/String
def site(text):
    Fixer.log('Ya.Каталог')
    param = getparams(text)
    if len(param) < 2:
        Fixer.errProcess = Fixer.Process	
        return '#err: Нет второго параметра'
    if param[0].lower() == 'info':
        tsend = Ya.Catalog(param[1])
    elif param[0].lower() == 'find':
        tsend = Ya.FindCatalog(param[1])
    else: 
        Fixer.errProcess = Fixer.Process
        return '#err: Параметр "%s" не поддерживается!' % param[0]
    Fixer.log('Ya.Каталог', tsend)
    return tsend

# ---------------------------------------------------------
# сервис wiki : #wiki: query 
def wiki(text, send=False):
    Fixer.log('Wikipedia')
    if send: Bot.SendMessage('Секундочку! Ищу информацию в Википедии...')
    pages = Wiki.SearchPage(text.strip())
    if len(pages) == 0: return 'Я поискал информацию в Википедии, но ничего не нашёл. Можешь уточнить запрос?'
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    Fixer.log('Wikipedia', Fixer.htext)
    return Wiki.MiniContent(pages[0])
	
# ---------------------------------------------------------
# сервис wiki-more
def wikimore(text):
    Fixer.log('Wikipedia.More', text.strip())
    return Wiki.More(Fixer.Page)
	
# ---------------------------------------------------------
# сервис geowiki : #geowiki: [radius]
def geowiki(text, send=False):
    Fixer.log('WikipediaGeo')
    if text == '':
        rad = Fixer.Radius
    else:
        try:
            text += ' '
            rad = str(text[:text.find(' ')])
        except:
            Fixer.errlog('WikipediaGeo', 'Ошибка в определении радиуса: '+text[:text.find(' ')])
            rad = 100
    if send: Bot.SendMessage('Секундочку! Ищу ближайшие достопримечательности по Википедии...')
    pages = Wiki.GeoSearch(Fixer.X, Fixer.Y, resnom=10, rad=rad)
    if len(pages) == 0 or pages[0] == '#': return 'Я поискал достопримечательности в Википедии, но ничего не нашёл. Может стоит величить радиус поиска?'
    s = 'Нашёл следующие достопримечательности:\n'
    for p in pages:
        s += p + '\n'
    Bot.SendMessage(s)
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    Fixer.log('WikipediaGeo', Fixer.htext)
    return Wiki.GeoFirstMe(rad)

# ---------------------------------------------------------
# сервис geowiki1 : #geowiki1: [radius]
def geowiki1(text, send=False):
    Fixer.log('WikipediaGeo1')
    if text == '':
        rad = Fixer.Radius
    else:
        try:
            text += ' '
            rad = str(text[:text.find(' ')])
        except:
            Fixer.errlog('WikipediaGeo1', 'Ошибка в определении радиуса: '+text[:text.find(' ')])
            rad = 100
    if send: Bot.SendMessage('Секундочку! Ищу ближайшую достопримечательность по Википедии...')
    response = Wiki.GeoFirstMe(rad)
    if response[0] == '#': return 'В радиусе '+str(rad)+' метров не нашёл ни одной достопримечательности :('
    pages = Wiki.GeoSearch(Fixer.X, Fixer.Y, resnom=10, rad=rad)
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    Fixer.log('WikipediaGeo1', Fixer.htext)
    return response

# ---------------------------------------------------------
# сервис google.Define : #define: word
def define(text):
    Fixer.log('Google.Define')
    stext = Google.Define(text.strip())
    Fixer.log('Google.Define', stext)					
    return stext

# ---------------------------------------------------------
# сервис google.Calc : #calc: formula
def calc(text):
    Fixer.log('Google.Calc')
    stext = Google.Calc(text.strip())
    Fixer.log('Google.Calc', stext)					
    return stext

# ---------------------------------------------------------
# сервис google : #google: query / [$responce]
def google(text, map=False):
    Fixer.log('Google.Search')
    if text == '$responce': text = Fixer.Query
    print(text)
    stext = Google.Search(text.strip(), bmap=map)
    Fixer.log('Google.Search', stext)					
    return stext

# ---------------------------------------------------------
# сервис getcoords
def getcoords(geocity):
    if geocity.strip() == '': geocity = 'LOCATION'
    if geocity.strip().upper() == 'LOCATION':
        Fixer.Coords[0] = Fixer.X
        Fixer.Coords[1] = Fixer.Y
        s = 'LOCATION'
    else:
        s = Ya.Coordinates(geocity)
    print(s)
    return s

# ---------------------------------------------------------
# сервис weather : #weather: type:full/short/day/cloud/wind/sun/night/riseset/temp | $geo-city | $date
def weather(text):
    Fixer.log('Weather')
    params = getparams(text)
    #print(params)
    if len(params) < 2: params.append('Location')
    if len(params) < 3: params.append(str(Fixer.Date))
    #print('{%s}' % params[1])
    s = getcoords(params[1])
    #print('{%s}' % s)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.Forecast(Fixer.Coords[0], Fixer.Coords[1], params[2])
    print(m)
    if m[0] == '#': return m
    stext = ''
    if params[0] == 'full': # полный прогноз погоды
        stext = m[17] + '\n\n' + m[18] + '\n\n' + m[19]
    elif params[0] == 'day': # полный прогноз погоды (день)
        stext = m[18]
    elif params[0] == 'night': # полный прогноз погоды (ночь)
        stext = m[19]
    elif params[0] == 'short': # короткий прогноз погоды
        s = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
        s += 'Днём: ' + m[3] + '\n'
        s += 'Ночью: ' + m[11]
        stext = s
    elif params[0] == 'temp': # температура
        stext = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
    elif params[0] == 'riseset': # восход и заход солнца
        stext = 'Рассвет: ' + m[0] + '\n'
        stext += 'Закат: ' + m[1]
    elif params[0] == 'cloud': # осадки, облачность
        s = 'Днём: ' + m[3]
        s += ', вероятность осадков ' + m[4] + '\n'
        s += 'Объём осадков: ' + m[5] + '\n'
        s += 'Продолжительность осадков: ' + m[6] + '\n'
        s += 'Облачность: ' + m[7] + '\n'
        s += '\nНочью: ' + m[11]
        s += ', вероятность осадков ' + m[12] + '\n'
        s += 'Объём осадков: ' + m[13] + '\n'
        s += 'Продолжительность осадков: ' + m[14] + '\n'
        s += 'Облачность: ' + m[15]
        stext = s
    elif params[0] == 'wind': # ветер
        s = 'Днём: ' + m[8]
        s = '\nНочью: ' + m[16]
        stext = s
    elif params[0] == 'sun': # солнце
        stext = 'Днём: ' + m[3] + ', солнечные часы - ' + m[9]
    else: # необрабатываемый случай
        stext = '#problem: {' + params[0] + '}'
    Fixer.log('Weather', stext)					
    return stext

# ---------------------------------------------------------
# сервис timezone : #timezone: [$geo-city]
def timezone(text):
    Fixer.log('TimeZone')
    #if text.strip() == '': text = 'Location' - уже есть в getcoords
    s = getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    if m[0][0] == '#':
        # попытка узнать часовой пояс из Geo
        s = Geo.GetTimezone(Fixer.Coords[0], Fixer.Coords[1])
        #print(s)
        return s
    #ss = 'Часовой пояс: '
    ss = ''
    if float(m[5]) > 0: ss = '+'
    Fixer.log('TimeZone', ss)	
    return ss + m[5]

# ---------------------------------------------------------
# сервис population : #population: [$geo-city]
def population(text):
    Fixer.log('Population')
    #if text.strip() == '': text = 'Location' - уже есть в getcoords
    s = getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    #print(m)
    if m[0][0] == '#': return m[0]
    s = 'Население пункта ' + m[2] +' ['+m[1]+'] '+m[3]+' ('+m[4]+') : '+str(m[7])+' чел.'
    Fixer.log('Population', s)	
    return s

# ---------------------------------------------------------
# сервис elevation : #elevation: [$geo-city]
def elevation(text):
    Fixer.log('Elevation')
    #if text.strip() == '': text = 'Location'-  - уже есть в getcoords
    s = getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    print(m)
    if m[0][0] == '#': return m[0]
    s = 'Высотная отметка ' + m[2] +' ['+m[1]+'] '+m[3]+' ('+m[4]+') : '+str(m[6])+' метров над уровнем моря'
    Fixer.log('Elevation', s)	
    return s

# ---------------------------------------------------------
# сервис geodistance : #geodistance: $geo-city1 - [$geo-city2]
def geodistance(text):
    Fixer.log('GeoDistance')
    params = getparams(text)
    if len(params) < 2: params.append('Location')
    s = getcoords(params[0])
    if s[0] == '#': return 'Не удалось распознать первый город или найти его координаты :( - ' + s
    x = Fixer.Coords[0]; y = Fixer.Coords[1]
    s = getcoords(params[1])
    if s[0] == '#': return 'Не удалось распознать второй город или найти его координаты :( - ' + s
    s = str(round(Geo.Distance(y, x, Fixer.Coords[1], Fixer.Coords[0]))) + ' км по прямой линии'
    Fixer.log('GeoDistance', s)
    return s

# ---------------------------------------------------------
# сервис compliment : #compliment:
def compliment():
    Fixer.log('Comliment')
    if Fixer.Type == 1:
        stext = random.choice(Fixer.mCompliment[1])
    else:
        stext = random.choice(Fixer.wCompliment[1])
    Fixer.log('Comliment', stext)
    return stext
	
# ---------------------------------------------------------
# сервис anecdote : #anecdote:
def anecdote():
    Fixer.log('Fun.Anecdote')
    stext = Fun.Anecdote()
    Fixer.log('Fun.Anecdote', stext)
    return stext

# ---------------------------------------------------------
# сервис rate
def rate(text):
    Fixer.log('Rates.Rate')
    params = getparams(text)
    if params[0] == 'ALL': # если нужны курсы всех валют
        stext = Fixer.Dialog('rate')
        for val in Fixer.Valutes:
            stext += '\n' + Fixer.Valutes[val] + ' : ' + Rate.RateRubValue(val, params[1], float(params[2])) + ' ' + Fixer.valutes[params[1]]
    else:
        stext = Rate.RateRubValue(params[0], params[1], float(params[2])) + ' ' + Fixer.valutes[params[1]]
        if stext[0] != '#': Fixer.LastValute.append(params[0])
    Fixer.log('Rates.Rate', stext)
    return stext

# ---------------------------------------------------------
# сервис setrate
def setrate(text):
    Fixer.log('SetRate', text)
    if Rate.isValute(text) == False: return 'Не знаю такой валюты: ' + text
    Fixer.Valute = text
    return 'Хорошо! Установлена валюта по-умолчанию: ' + Fixer.Valutes[text]

# ---------------------------------------------------------
# сервис note - #notes: ALL/<Имя раздела> | Текст
def note(text):
    Fixer.log('Note', text)
    params = getparams(text)
    Fixer.Notes[params[0].upper()] = params[1]
    return Fixer.Dialog('note_section') + params[0].upper()

# ---------------------------------------------------------
# сервис notes - #notes: [ALL/<Имя раздела>]
def notes(text):
    text = text.strip()
    Fixer.log('Notes', text)
    if text.upper() == 'ALL' or text == '':
        s = Fixer.Dialog('notes_all')
        for snote in Fixer.Notes.values():
            s += '\n' + snote
    else:
        s = Fixer.Dialog('notes_section') + text.upper()
        for snote in Fixer.Notes[text.upper()]:
            s += '\n' + snote
    return s

# ---------------------------------------------------------
# сервис setlocation
def setlocation(text):
    Fixer.log('SetLocation')
    from geolocation.main import GoogleMaps
    try:
        params = getparams(text, separator=',')
        Fixer.LastX.append(Fixer.X)
        Fixer.LastY.append(Fixer.Y)
        Fixer.Y = params[0]
        Fixer.X = params[1]
        mes = 'Хорошо! Установлены координаты: ' + Fixer.Y + ', ' + Fixer.X + '.\n'
        # Сервис Google.Geocoding
        my_location = GoogleMaps(api_key=config.GMaps_key).search(lat=Fixer.Y, lng=Fixer.X).first()
        mes += my_location.formatted_address #+ '\n'
        Fixer.Address = my_location.formatted_address
        Fixer.LastAddress.append(Fixer.Address)
        return mes
    except Exception as e:
        Fixer.errlog('SetLocation', str(e))
        return '#bug: ' + str(e)
	
# ---------------------------------------------------------
# сервис correction
def correction(text):
    Fixer.log('Correction', text)
    Fixer.NewDialogs[Fixer.strCleaner(Fixer.Query)] = getparams(text, ';')
    Fixer.Save(Fixer.NewDialogs, 'NewDialogs')
    s = '\nНа запрос: ' + Fixer.strCleaner(Fixer.Query)
    for i in getparams(text, ';'):
        s += '\nВариант ответа: '+ i
    Bot.SendAuthor('Уведомление от пользователя ' + str(Fixer.UserID) + s)
    s = Fixer.Dialog('correction') + s
    Fixer.bAI = True; Fixer.Service = 'ai'; Fixer.Conext = False
    return s

# ---------------------------------------------------------
# сервис date / time / datetime : location - type
def datetime(location, ttype='datetime'):
    Fixer.log('DateTime: %s | %s' % (location, ttype))
    #s = Ya.Coordinates(location)
    tz = float(timezone(location))
    import datetime
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=tz)
    if ttype == 'time':
        #print('time')
        return now.strftime('%H:%M:%S')
    elif ttype == 'date':
        #print('date')
        return now.strftime('%Y-%m-%d')
    else:
        return now.strftime('%Y-%m-%d %H:%M:%S')

# ---------------------------------------------------------
# сервис log / logerr : число последних записей
def log(snumber, etype='none'):
    Fixer.log('log')
    mlog = []
    try:
        if etype == 'err':
            f = open('log_error.txt', encoding='utf-8')
            for line in f:
                mlog.append(line)
            f.close()
        else:
            f = open('log.txt', encoding='utf-8')
            for line in f:
                mlog.append(line)
            f.close()
        ilen = len(mlog)
        try:
            number = int(snumber)
        except:
            number = 10
        if number < 1: number = 1
        if number > 100: number = 100
        if ilen < number: start = 0
        else: start = ilen - number
        s = ''
        for i in range(start, ilen):
            s += '[%i] %s' % (i, mlog[i])
        return s
    except Exception as e:
        Fixer.errlog('log','Ошибка при загрузке логов: ' + str(e))

# ---------------------------------------------------------
# сервис buglog : #buglog: numberStart | numberEnd
def buglog(text):
    from DB.SQLite import SQL
    Fixer.log('buglog')
    params = getparams(text)
    if len(params) < 2: params.append(params[0])
    m = SQL.sql('SELECT * FROM bugs WHERE id >= %s AND id <= %s' % (params[0], params[1]))
    send = ''
    if len(m) > 0:
        for im in m:
            if im[1] == 1: send += '\nBUG'
            elif im[1] == 2: send += '\nPORBLEM'
            else: send += '\nANOTHER'
            send += '[%i]: %s\nQuery: %s\nProcess: %s\nResponce: %s' % (im[0],im[5],im[2],im[3],im[4])
    else: # если нет результата
        send += 'Баги №№ %s - %s не найдены!' % (params[0], params[1])
    return send

# ---------------------------------------------------------
# сервис RSS : #rss: rssurl | numberpost(3)
def rss(text):
    Fixer.log('RSS')
    params = getparams(text)
    params[0] = params[0].lower() # форматирование строки
    if len(params) < 2: params.append('3')
    titles = RSS.GetTitles(params[0])
    if titles['status'] == 'ok':
        stext = '%s\n%s\nЯзык публикации: %s\nАвтор: %s\nСайт: %s' % (titles['title'], titles['subtitle'], titles['lang'], titles['author'], titles['link'])
        posts = RSS.GetPosts(params[0])
        for i in range(0, int(params[1])):
            stext += '\n\n[%s]\n%s\n(%s)\n%s' % (posts[i]['title'], posts[i]['description'], posts[i]['date'], posts[i]['link'])
        Bot.SendMessage(stext)
        brss = True
        for rss in Fixer.RSS:
            if params[0] == rss['rss']: brss = False
        smess = ''
        if brss: # записываем rss-канал
            drss = {}
            drss['rss'] = params[0]
            drss['title'] = titles['title']
            drss['posts'] = []
            for post in posts:
                dpost = {}
                dpost['len'] = len(post['description'])
                dpost['date'] = post['date']
                drss['posts'].append(dpost)
            Fixer.RSS.append(drss)
            Fixer.LastRSS.append(params[0])
            smess = 'RSS-канал "%s" успешно поключен!\nНовости канала будут приходить по мере их поступления.' % titles['title']
            from datetime import datetime, timedelta
            now = (datetime.today() + timedelta(minutes=1)).strftime('%H:%M:%S') # форматирование времени
            task('RSS | ' + now + ' | 0 | #rss-news: ' + params[0])
        else: smess = 'RSS-канал "%s" был сохранён ранее.' % titles['title']

        return smess
    else: return 'указанная ссылка не является RSS-каналом.'

# ---------------------------------------------------------
# сервис RSS-news : #rss-news: rssurl
def rssnews(url):
    Fixer.log('RSS-News')
    url = url.lower() # форматирование строки
    s = '#null' # 'Не удалось найти rss-канал в подписке: ' + url
    oldposts = [] # поиск старых постов
    iRSS = 0
    for rss in Fixer.RSS:
        if url == rss['rss']:
            oldposts = rss['posts']
            s = 'Новости rss-канала "%s":' % rss['title']
            posts = RSS.GetNewPosts(url, oldposts)
            if len(posts) > 0:
                for post in posts:
                    s += '\n\n[%s]\n%s\n(%s)\n%s' % (post['title'], post['description'], post['date'], post['link'])
                    dpost = {} # запись новостей
                    dpost['len'] = len(post['description'])
                    dpost['date'] = post['date']
                    Fixer.RSS[iRSS]['posts'].append(dpost) # добавление в Fixer
                #print(Fixer.RSS)
                Chat.Save()
            else:
                s = '#null'
            break
        iRSS += 1
    return s

# ---------------------------------------------------------
# сервис RSS-all : #rss-all: 
def rssall():
    Fixer.log('RSS-all')
    s = 'Список всех подключённых rss-каналов:'
    iRSS = 0
    for rss in Fixer.RSS:
        s += '\n[%i] %s - %s' % (iRSS, rss['rss'], rss['title'])
        iRSS += 1
    if iRSS == 0: s += '\n( список пуст )'
    else: s += '\n\nМожно удалить лишние каналы командой "rss-del: №"'
    return s

# ---------------------------------------------------------
# сервис RSS-del : #rss-del: №
def rssdel(text):
    Fixer.log('RSS-del')
    irss = int(text)
    s = 'Удаление канала "%s" прошло успешно!' % Fixer.RSS[irss]['title']
    del(Fixer.RSS[irss])
    return s

# ---------------------------------------------------------
# сервис IATA : #IATA: №
def iata(text, stype='code'):
    Fixer.log('IATA')
    colsReturn = ['code', 'name', 'cityName', 'timeZone', 'country', 'lat', 'lon',
                 'runwayLength', 'runwayElevation', 'phone', 'email', 'website']
    sfrm = '%0 - %1, г. %2, %4 (%3)\nДлина взлётной полосы: %7, высотная отметка: %8\nТелефон: %9, e-mail: %%10\nURL: %%11'
    s = ''; s2 = ''
    if stype == 'code':
        m1 = IATA.Airport(code=text)
        m2 = IATA.City(code=text)
        if len(m2) > 0:
            s += Fixer.strFormat(m2, sformat=sfrm, sobj ='аэропортов в городах') + '\n'
        s += '\n' + Fixer.strFormat(m1, sformat=sfrm, sobj ='отдельных аэропортов')
    elif stype == 'air':
        m = IATA.Airport(name=text)
        s = Fixer.strFormat(m, sformat=sfrm, sobj ='аэропортов')
    elif stype == 'city':
        m = IATA.City(name=text)
        s = Fixer.strFormat(m, sformat=sfrm, sobj ='аэропортов в городах')
    elif stype == 'code3':
        if Word.Type(text) == 50: m = IATA.Country(code=text) # если латиница
        else: m = IATA.Country(name=text)
        s = Fixer.strFormat(m, sformat='код: %0, код3: %1, iso: %2\nназвание: %3', sobj ='стран')
    return s

# ---------------------------------------------------------
# сервис skill : #skill:
def skill():
    Fixer.log('skill')
    m = [] # массив сервисов
    for skey in Fixer.Services:
        m.append(skey)
    ser = random.choice(m)
    print(ser)
    s = 'Сервис "%s" - %s\nАвтор: %s\n' % (Fixer.Services[ser][1], Fixer.Services[ser][4], Fixer.Services[ser][2])
    s += 'Примеры: '
    for pr in Fixer.Services[ser][7]:
        s += '"%s", ' % pr
    s = s[:-2]
    return s

# ---------------------------------------------------------
# сервис morph : #morph: слово или предложение
def morph(text):
    Fixer.log('morph')
    s = ''
    if ' ' in text: # несколько слов
        words = String.GetWords(text)
        for word in words:
            s += Word.Morph(word) + '\n'
    else:
        s = Word.Morph(text)
    return s

# ---------------------------------------------------------
# Обработчик сервисов - на вход строка с сервисом (#servicename:)
# ---------------------------------------------------------
def ServiceProcess(response):
    ser, send = Fixer.servicefind(response)
    if ser == '': # не найден сервис в описании
        return '#problem: Сервис {%s} не зарегестрирован!' % Fixer.Service
    # Запуск сервиса Task (Задача для уведомления пользователя)
    if ser == '#task:': tsend = task(send)
    # Запуск сервиса Answer (Диалог с пользователем)
    elif ser == '#answer:': tsend = answer(send)
    # Запуск сервиса Fixer (информация)
    elif ser == '#fixer:': tsend = fixer(send)
    # Запуск сервиса Name
    elif ser == '#name:': tsend = name(send)
    # Запуск сервиса User
    elif ser == '#user-age:': tsend = user('age', send)
    elif ser == '#user-name:': tsend = user('name', send)
    elif ser == '#user-type:': tsend = user('type', send)
    elif ser == '#user-birthday:': tsend = user('birthday', send)
    elif ser == '#user-family:': tsend = user('family', send)
    elif ser == '#user-phone:': tsend = user('phone', send)
    elif ser == '#user-email:': tsend = user('email', send)
    elif ser == '#user-interest:': tsend = user('interest', send)
    elif ser == '#user-contact:': tsend = user('contact', send)
    elif ser == '#user-thing:': tsend = user('thing', send)
    # Запуск сервиса Acquaintance
    elif ser == '#acquaintance:': tsend = acquaintance()
    # Запуск сервиса Booking
    elif ser == '#booking:': tsend = booking(send, send=True) 
    # Запуск сервиса Яндекс.Расписание
    elif ser == '#timetable:': tsend = timetable(send, send=True)
    # Запуск сервиса Яндекс.Переводчик
    elif ser == '#translate:': tsend = translate(send)    
    # Запуск сервиса Яндекс поиск объектов
    elif ser == '#object:': tsend = yaobject(send)
    # Запуск сервиса Яндекс.Координаты
    elif ser == '#coordinates:': tsend = coordinates(send)
    # Запуск сервиса Яндекс.Каталог
    elif ser == '#site:': tsend = site(send)
    # Запуск сервиса Wikipedia - поиск информации 
    # #wiki: <название>
    elif ser == '#wiki:': tsend = wiki(send, send=True)
    # Запуск сервиса Wikipedia - поиск ближайших достопримечательностей 
    # #geowiki: <радиус, метры>
    elif ser == '#geowiki:': tsend = geowiki(send, send=True)
    # Запуск сервиса Wikipedia - поиск ближайшей достопримечательности
    # #geowiki1: <радиус, метры>
    elif ser == '#geowiki1:': tsend = geowiki1(send, send=True)
    # Запуск сервиса Wikipedia - поиск дополнительной информации 
    # #wikimore: <название>
    elif ser == '#wiki-more:': tsend = wikimore(send)
    # Запуск сервиса Google
    elif ser == '#google-map:': tsend = google(send, map=True)
    elif ser == '#google:': tsend = google(send)
    # Запуск сервиса Google.Define
    elif ser == '#define:': tsend = define(send)
    # Запуск сервиса Google.Calc
    elif ser == '#calculator:': tsend = calc(send)
    # Запуск сервиса Weather
    elif ser == '#weather:': tsend = weather(send)
    # Запуск сервиса TimeZone
    elif ser == '#timezone:': tsend = timezone(send)
    # Запуск сервиса Population
    elif ser == '#population:': tsend = population(send)
    # Запуск сервиса Elevation
    elif ser == '#elevation:': tsend = elevation(send)
    # Запуск сервиса GeoDistance
    elif ser == '#geodistance:': tsend = geodistance(send)
    # Запуск сервиса Fun
    # #Compliment: 
    elif ser == '#compliment:': tsend = compliment()
    # #anecdote: 
    elif ser == '#anecdote:': tsend = anecdote()
    # Запуск сервиса Rate
    # #rate: 
    elif ser == '#rate:': tsend = rate(send)
    elif ser == '#setrate:': tsend = setrate(send) 
    # Запуск локального сервиса Notes
    # #note: 
    elif ser == '#note:': tsend = note(send)
    elif ser == '#note-all:': tsend = notes(send)
    # сервис геолокации Телеграм
    # #location: <текст>
    elif ser == '#location:': return '#LOC! ' + send
    # Сервис установки координат
    elif ser == '#setlocation:': tsend = setlocation(send)
    # Сервис корректировки ответов
    elif ser == '#correction:': tsend = correction(send)
    # Сервис времени и даты
    elif ser == '#time:': tsend = datetime(send, 'time')
    elif ser == '#date:': tsend = datetime(send, 'date')
    elif ser == '#datetime:': tsend = datetime(send)
    # Сервис логов и багов
    elif ser == '#log:': tsend = log(send)
    elif ser == '#errlog:': tsend = log(send, etype='err')
    elif ser == '#buglog:': tsend = buglog(send)
    # Сервис RSS
    elif ser == '#rss:': tsend = rss(send)
    elif ser == '#rss-news:': tsend = rssnews(send)
    elif ser == '#rss-all:': tsend = rssall()
    elif ser == '#rss-del:': tsend = rssdel(send)
    # Сервис IATA
    elif ser == '#iata:': tsend = iata(send)
    elif ser == '#iata-air:': tsend = iata(send, 'airport')
    elif ser == '#iata-city:': tsend = iata(send, 'city')
    elif ser == '#code3:': tsend = iata(send, 'code3')
    # Сервис информирования о возможностях
    elif ser == '#skill:': tsend = skill()
    # Сервис морфологического анализа
    elif ser == '#morph:': tsend = morph(send)
    # Спецсервис для кодирования
    elif ser == '#code:': tsend = str(DefProcess.Code(send))
    # Сервисы DaData
    elif ser == '#dataname:': tsend = strData.Name(send, False)
    elif ser == '#dataaddress:': tsend = strData.Address(send, False)
    elif ser == '#dataorg:': tsend = strData.Organization(send, False, False)
    elif ser == '#dataorgid:':
        print(send)
        tsend = strData.Organization(send, True, False)

    # Все остальные случаи
    else: tsend = '#problem: Сервис {%s} не найден!' % Fixer.Service
    return tsend

# ---------------------------------------------------------
# Основной обработчик пользовательских запросов
# ---------------------------------------------------------
def FormMessage(text):
    cl = 0
    while cl < 3:
        cl += 1
        # Автовключение сервиса
        if text[0] == '#': Fixer.bAI = False # принудительно отключаем ИИ        
        # Включение сервиса принудительной контекстной зависимости
        if Fixer.Context and Fixer.Service != '':
            print('Сработала контекстная зависимость! Включён сервис #' + Fixer.Service)
            text = '#'+Fixer.Service+': ' + text
            if text[0] == '#': Fixer.bAI = False # принудительно отключаем ИИ
        # Проверяем что ИИ отключен правильно (например, для разового запуска сервиса)
        if Fixer.bAI == False: 
            if  Fixer.Service != '':
                if text[0] != '#':
                    print('Разово запущен сервис #' + Fixer.Service)
                    text = '#'+Fixer.Service+': ' + text
            else:
                # непонятно почему отключён ИИ ?
                print('Принудительное включение AI!')
                Fixer.bAI = True # принудительное включение ИИ
        else:
            print('Включён AI!')
            Fixer.Context = False
        if Fixer.bAI: # Если включён ИИ
            response = ai(text)
        else: # Если выключен ИИ
            response = text
            Fixer.bAI = True # Включаем ИИ на тот случай, если произойдёт ошибка
        # Если есть ответ от бота - присылаем юзеру, если нет - ИИ его не понял
        if response:
            # Ищем сервисы для включения #
            if response.find('#') > 0 and response[0] != '#': # Если есть последовательный сервис
                t = response.find('#')
                Bot.SendMessage(response[:t])
                response = response[t:]
            #Fixer.log('ai', 'Сообщение ИИ: ' + response)
            tsend = '*' # проверка на обработку сервисом
            if response[0] == '#' and response[:5] != '#bug:': # Признак особой обработки - запуск определённого сервиса
                if Fixer.Service != response[1:response.find(': ')]: # Сброс контекста если вызван другой сервис
                    Fixer.Context = False
                Fixer.Service = response[1:response.find(': ')]
                #print('Текущий сервис: {' + Fixer.Service + '}')
                Fixer.Query = text # сохраняем последний запрос пользователя
                ### Запуск обработчика сервисов ###
                tsend = ServiceProcess(response)
                ### обработка результатов сервисов ###
                if tsend == '': tsend = '#problem: null result'
                if tsend == '#null': return '' # для пустых уведомлений
                try: # проверка на корректность ответа
                    if tsend[0] == '*': 
                        Fixer.log('Processor', 'Cервис не найден: ' + response[0:response.find(':')])
                        return Fixer.Dialog('no_service') + response #[0:response.find(':')])
                except:
                    tsend = '#bug: responce type [%s] = %s' % (str(type(tsend)),str(tsend))
                return tsend           
            else:
                # Если ответ ИИ не требует обработки - отсылаем пользователю
                Fixer.Query = text # сохраняем последний запрос пользователя
                Fixer.log('Processor', 'Ответ пользователю: ' + response)
                Fixer.Service = 'ai'
                return response
        else: # не удалось ответить
            # Не удалось ответить
            s = text
            # Попробуем найти в вики
            if len(text) < 20 and text.endswith('?') == False: 
                s = wiki(text)
                if s[0] != '#':
                    return s
                else:
                    Fixer.htext = ''
                    s = text
            # Попробуем найти в ответах
##            elif text.endswith('?'):
##                s = Web.Otvet(text)
##                if s[0] != '#': return s
            # Попробуем найти в поисковике Google 
            s = google(text)
            if s[0] != '#':
                return s
            else:
                Fixer.htext = ''
            s = Fixer.strCleaner(text)
            # Ищем среди новых диалогов
            for i in Fixer.NewDialogs:
                if i == s: return random.choice(Fixer.NewDialogs[i]) # удалось найти среди новых диалогов
            Fixer.log('Ответ пользователю: Извини, я тебя не понял...')
            # Bot.SendMessage(Fixer.Dialog('null'))
            Fixer.Query = text # сохраняем последний запрос пользователя
            #Fixer.Service = 'correction'
            Fixer.bAI = False
            return Fixer.Dialog('null')  # Fixer.Dialog('new_dialog')
