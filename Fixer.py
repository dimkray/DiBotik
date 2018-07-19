# -*- coding: utf-8 -*-
from datetime import datetime, date
from DB.SQLite import SQL
import json
import pickle
import os

# текущая база данных
DB = 'DB/bot.db'

# общие фразы
responses = ['yesno','wait','notice']
# Загрузка всех словарей в конце файла

Response = '' # статус диалога с пользователем
Query = '' # последний запрос пользователя

# уведомление пользователя вкл/выкл
bNotice = True

# Процессорные фиксаторы
bAI = True # Признак включения сервиса ИИ

# текущая версия
Version = 20180427

# общие фиксаторы
Time = []     # фиксация времени
Chat = []     # история чата
UserID = 0   # текущий пользователь
ChatID = 0    # Текущий чат
PeerID = 0    # Текущее назначение - для беседы, для группы
bChats = 0    # Признак беседы: 0 - не беседа, 1 - беседа, 2 - беседа, где надо ответить
Name = 'человек'     # имя
Family = 'без фамилии'   # фамилия
BirthDay = 'день рождения не известен' # ДР
Phone = 'телефон не указан'    # номер телефона
eMail = 'e-mail не указан'    # почта
Contacts = {} # Мессенджеры
Interests = []# Список интересов
Things = []   # Список вещей/характеристик пользователя
Age = 0       # 0 - неизвестно
Type = 0      # 0 - неизвестно, 1 - мужчина, 2 - женщина
Thema = ''    # текущая тема
LastThema = []
Mess = '' # текущий мессенджер
TimeZone = 3  # часовой пояс пользователя относительно UTF

Process = '' # текущий процесс
errProcess = '' #процесс, в котором возникла ошибка
errMsg = '' #сообщение об ошибке

bNow = False # признак сейчас
Date = date.today()

Service = '#' # текущий сервис
Context = False
LastService = []

Radius = 100 # радиус интресера

def KnowUser(): # возвращает процент информации о пользователе
    rez = 0
    if Name != '': rez += 20
    if Family != '': rez += 10
    if BirthDay != '': rez += 10
    if Phone != '': rez += 10
    if eMail != '': rez += 10
    if Age > 0: rez += 10
    if Type > 0: rez += 10
    if len(Contacts) > 0: rez += 10
    if len(Interests) > 0: rez += 10
    return rez

htext = ''    # гиперссылка

# сервис Локация
X = 37.618912 # global latitude
Y = 55.751455 # global longitude
LastX = []
LastY = []
Address = 'адрес не указан'
LastAddress = []
Coords = [X, Y] # координаты города
LastCoords = []

# сервис Яндекс.Переводчик
Lang1 = 'авто'    # lang-from
Lang2 = 'английский'    # lang-tobytes
Ttext = ''    # переводимый текст
LastLang1 = []
LastLang2 = []

# сервис Яндекс.Расписание
nameSt = 'Москва'   # текущая станция
region = 'Москва'   # регион поиска
iTr = 0       # тип транспорта
St1 = 'Москва'      # станция отправления
St2 = ''      # станция прибытия
trDate = ''   # интересующая дата
LastSt1 = []
LastSt2 = []
LastTr = []

# сервис Wikipedia
WikiStart = 0
Page = 'Москва'
LastPage = []

# сервис Rate
Valute = 'RUB' # актуальная валюта
LastValute = []

# Сервис Яндекс поиск объектов
Obj = [] # Подробный список найденных объектов
sObj = [] # Список преобразованный в строку

# Сервис Notes
Notes = {} # Записи пользователя

# Сервис RSS-каналов
RSS = []
LastRSS = []

# Запись лога
def log(process, s = ''):
    f = open('log.txt', 'a', encoding='utf-8')
    Process = process
    if s:
        try:
            s = s.replace('\n',' \ ')
            f.write('%s %s {%s}: %s\n' % (str(datetime.today()), UserID, Process, s))
            print('{%s}: %s' % (Process, s))
        except Exception as e:
            print('Ошибка при попытке записи лога! ' + str(e))
    f.close()

# Запись лога ошибок
def errlog(errprocess, s):
    f = open('log_error.txt', 'a', encoding='utf-8')
    try:
        s = s.replace('\n',' \ ')
        errProcess = errprocess
        f.write('%s %s {%s}: %s\n' % (str(datetime.today()), UserID, errProcess, s))
        print('Ошибка! {%s}: %s' % (errProcess, s))
        errMsg = s
    except Exception as e:
        print('Ошибка при попытке записи лога! ' + str(e))
    f.close()

# Запись времени и даты
def time():
    s = str(datetime.today())
    return s[0:s.find('.')]


# Функция проверки существования файла
def Exists(path):
    try:
        os.stat(path)
    except OSError:
        return False
    return True

# Функция записи словаря
def Save(dictionary, name):
    try:
        f = open('DB/' + name + '.json', 'w', encoding='utf-8')
        json.dump(dictionary, f, sort_keys=False, ensure_ascii=False)
        f.close()
        return True
    except Exception as e:
        errlog('Fixer.Save', name + '.json - ' + str(e))
        return False

# Функция загрузки словаря
def Load(name):
    try:
        dictionary = {}
        if Exists('DB/' + name + '.json') == False: return dictionary
        f = open('DB/' + name + '.json', 'r', encoding='utf-8')
        dictionary = json.load(f)
        return dictionary
    except Exception as e:
        errlog('Fixer.Load', name + '.json - ' + str(e))
        return dictionary

# Функция записи словаря в байты
def SaveB(dictionary, name):
    try:
        f = open('DB/' + name + '.db', 'wb')
        pickle.dump(dictionary, f)
        f.close()
        return True
    except Exception as e:
        errlog('Fixer.SaveB', name + '.db - ' + str(e))
        return False

# Функция загрузки словаря из байт
def LoadB(name):
    try:
        dictionary = {}
        if Exists('DB/' + name + '.db') == False: return dictionary
        f = open('DB/' + name + '.db', 'rb')
        dictionary = pickle.load(f)
        f.close()
        return dictionary
    except Exception as e:
        errlog('Fixer.LoadB', name + '.db - ' + str(e))
        return dictionary

# ---------------------------------------------------------
# вн.сервис Dialog - использование внутреннего диалога
def Dialog(key):
    import random
    if key in dialogs:
        return random.choice(dialogs[key])
    else:
        errlog('Fixer.Dialog', 'не найден ключ: ' + key)
        return key		
	
# ---------------------------------------------------------
# вн.сервис substitution - подстановка строковых переменных
def Subs(text):
    t = 0
    text = text.replace('\\n','\n')
    while text.find('[', t) >= 0:
        t1 = text.find('[', t)
        t2 = text.find(']', t1)
        s = text[t1:t2+1]; ss = ''
        if s.lower() == '[service]': ss = Service
        if s.lower() == '[thema]': ss = Thema
        if s.lower() == '[userid]': ss = UserID
        if s.lower() == '[chatid]': ss = str(ChatID)
        if s.lower() == '[name]': ss = Name
        if s.lower() == '[family]': ss = Family
        if s.lower() == '[birthday]': ss = BirthDay
        if s.lower() == '[phone]': ss = Phone
        if s.lower() == '[email]': ss = eMail
        if s.lower() == '[age]': ss = str(Age)
        if s.lower() == '[contacts]':
            for i in Contacts:
                ss += i + ': ' + Contacts[i] + '\n'
            ss = ss[:-2]
        if s.lower() == '[interests]':
            for i in Interests:
                ss += i + ', '
            ss = ss[:-2]
        if s.lower() == '[things]':
            for i in Things:
                ss += i + ', '
            ss = ss[:-2]
        if s.lower() == '[location]': ss = str(Y)+','+str(X)
        if s.lower() == '[address]': ss = Address
        if s.lower() == '[valute]': ss = Valute
        if s.lower() == '[home]': ss = Mess
        if s.lower() == '[notes]':
            for i in Notes:
                ss += i + ': ' + Notes[i] + '\n'
            ss = ss[:-2]
        if ss != '': text = text.replace(s, ss)
        t = t1 + 1
    #log('Fixer.Substitution', text)
    return text

# ---------------------------------------------------------
# вн.сервис strfind - поиск строки и обрезка по найденному (регистронезависимый)
def strfind(text, mfind, poz = 0):
    textU = text.upper()
    for sfind in mfind:
        ilen = len(sfind)
        if poz >= 0: # если ищем по тексту в определённой позиции
            if textU.find(sfind.upper()) == poz:
                return sfind, (text[:poz] + text[poz+ilen:]).strip() # вырезание
        else: # если ищем везде
            if textU.find(sfind.upper()) >= 0:
                while textU.find(sfind.upper()) >= 0:
                    text = text[:poz] + text[poz+ilen:] # вырезание
                    textU = text.upper()
                return sfind, text.strip()
    return '', text # ничего не нашлось

# ---------------------------------------------------------
# вн.сервис servicefind - поиск сервиса и обрезка по найденному (регистронезависимый)
def servicefind(text):
    m = [] # массив сервисов
    for skey in Services:
        m.append('#%s:' % skey)
        if len(Services[skey][9]) > 0: # если есть подсервисы
            for subser in Services[skey][9]:
                m.append('#%s-%s:' % (skey, subser))
    return strfind(text, m) # поиск сервиса

# ---------------------------------------------------------
# вн.сервис strcleaner - упрощение строки (убирает все лишние символы)
def strcleaner(text):
    text = text.strip().lower()
    text = text.replace('ё','е')
    text = text.replace('«','')
    text = text.replace('»','')
    text = text.replace('!','')
    text = text.replace('@','')
    text = text.replace('~','')
    text = text.replace('#','')
    text = text.replace('^','')
    text = text.replace('&','')
    text = text.replace('*','')
    text = text.replace('(','')
    text = text.replace(')','')
    text = text.replace('- ',' ')
    text = text.replace('+','')
    text = text.replace('=','')
    text = text.replace('{','')
    text = text.replace('}','')
    text = text.replace('[','')
    text = text.replace(']','')
    text = text.replace(';','')
    text = text.replace(':','')
    text = text.replace('?','')
    text = text.replace('<','')
    text = text.replace('>','')
    text = text.replace(',','')
    text = text.replace('.','')
    text = text.replace('`','')
    text = text.replace('\\','')
    text = text.replace('|','')
    text = text.replace('/','')
    text = text.replace('  ',' ')
    return text

# ---------------------------------------------------------
# вн.сервис strformat - преобразование результата в форматированный текст
def strformat(mresult, items = 5, sformat = '', nameCol = [], sobj = 'объектов'):
    if len(mresult) > 0: # если есть результат
        s = 'По запросу найдено %s: %i' % ( sobj, len(mresult)) 
        if items < len(mresult): s += '\nБудут показаны первые %i:' % items
        else: items = len(mresult)
        for i in range(0,items):
            if sformat == '': # если не задан формат
                if len(nameCol) > 1: # если несколько возвращаемых колонок
                    row = mresult[i]
                    s += '\n[%i] %s:' % (i+1, row[0])
                    ic = 0
                    for col in returnCol:
                        if col == 0: ic += 1; continue
                        s += '\n%s: %s' % (col, row[ic])
                        ic += 1              
                else: # если одна возвращаемая колонка
                    s += '\n[%i] %s' % (i+1, mresult[i])
            else: # если задан формат
                sitem = sformat
                row = mresult[i]
                while sitem.find('%%') >= 0:
                    x = sitem.find('%%')+2
                    r = int(sitem[x:x+2])
                    sitem = sitem.replace('%%'+str(r), str(row[r]))
                while sitem.find('%') >= 0:
                    x = sitem.find('%')+1
                    r = int(sitem[x:x+1])
                    sitem = sitem.replace('%'+str(r), str(row[r]))
                while sitem.find('\\%') >= 0:
                    sitem = sitem.replace('\\%', '%')
                s += '\n['+str(i+1)+'] ' + sitem
    else: s = 'По данному запросу нет результата :('
    return s

# ---------------------------------------------------------
# вн.сервис getparams - получение переменных в массив [] из строки переменных для сервиса
def getparams(text, separator='|'):
        if text.find(separator) < 0 and separator != ';' : # нет текущего сепаратора
            if text.find(' - ') > 0: separator = ' - '
            else:
                if text.find(',') > 0: separator = ','
                else: separator = ' '
        m = text.split(separator)
        x = 0
        for im in m:
            m[x] = im.strip() # убираем лишние пробелы
            x += 1
        return m

# ---------------------------------------------------------
# вн.сервис Sort для сортировки двухмерных массивов (сортировка по номеру колонки)
def Sort(massive, colnum, reverse = False):
    try:
        massive = sorted(massive, key=lambda st: st[colnum], reverse=reverse)
    except: pass
    return massive

# ---------------------------------------------------------
# вн.сервис inList - Добавление элемента в список (List), если его нет
def inList(mList, item):
    if item not in mList:
        mList.append(item)
    return mList

# ---------------------------------------------------------
# вн.сервис ListToDict - Преобразование двух списков в словарь внутри списка
def ListToDict(mNames, mRows, namesRez=[]):
    if namesRez == []: namesRez = mNames
    mRez = []; mIdx = []
    for name in namesRez:
        i = 0
        try:
            i = mNames.index(name)
        except: i = -1
        mIdx.append(i)
    for row in mRows:
        drow = {}
        i = 0
        for name in namesRez:
            if mIdx[i] >= 0:
                drow[name] = row[mIdx[i]]
            i += 1
        mRez.append(drow)
    return mRez

# Загрузка таблиц из БД
log('Fixer.Start', '------ Загрузка данных ------')
mCompliment = SQL.ReadAll('complimentMan')
wCompliment = SQL.ReadAll('complimentWoman')
Valutes = SQL.ReadDict('valutes')
valutes = SQL.ReadDict('valutes2')
yaLangs = SQL.ReadDict('yaLangs')
yaDirLang = SQL.ReadAll('yaDirLang')

# Пользовательские настройки сервисов
Settings = Load('DefSettings')

# Загрузка всех полезных словарей
Commands = Load('Commands')
Word1 = Load('Word1')
KeyWord = Load('KeyWord')
dialogs = Load('dialogs')
NewDialogs = Load('NewDialogs')
Services = Load('Services')
#Names = Load('Names')
log('Fixer.Start', 'Все словари загружены!')

# Создание базы данных
# import DB.CreateDB

# Обновление базы данных (из открытых источников)
# import DB.UpdateDB
