import Fixer
from DB.SQLite import SQL
from DB.SQLite import Finder
from Services.Yandex import Yandex
from Profiler import Profiler

stest = input('Введите запрос на поиск: ')

# здесь тестовая обработка #
##with Profiler() as p:
##    stest = SQL.sql(stest)

#print('Число строк в [anecdotes]: ' + str(SQL.Count('anecdotes')))
with Profiler() as p:
    print(Finder.strFind('RSS', ['rssUrl','link','titleU','subtitleU'],
                       '%'+stest+'%', returnCol=['rssUrl','link','title','subtitle'],
                       sFormat = '%2\nОписание: %3\nRSS-канал: %0\nСайт: %1'))
#print('Результат тестирования: найдено %i строк' % len(m))
#print(m)
#print(stest[0])

import time; time.sleep(5)
