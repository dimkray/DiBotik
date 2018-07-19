# -*- coding: utf-8 -*-
# Обновление базы данных DiBot из открытых источников

import Fixer
from Services.IATA import IATA
from DB.SQLite import SQL

def UpdateTable(NameTable, dCols, data):
    print('Удаление старой таблицы "%s"' % NameTable)
    print('Результат: ' + SQL.Delete(NameTable))
    print('Создание новой таблицы "%s"' % NameTable)
    print('Результат: ' + SQL.Table(NameTable, dCols))
    print('Запись данных: %i строк' % len(data))
    print('Результат: ' + SQL.WriteBlock(NameTable, data))
    print('-------------------------------------')

# основной блок программы
#----------------------------------

yn = input('...... Обновить таблицы и загрузить новые данные? Y/N: ')
if yn == 'Y': 

    # База аэропортов IATA
##    mAir = IATA.GetAirport()
##    if mAir[0] != '#':
##        Airs = []
##        for air in mAir:
##            mRow = []
##            mRow.append(air['code'])
##            mRow.append(air['name'])
##            mRow.append(air['name'].upper().replace('Ё','Е'))
##            Airs.append(mRow)
##        #UpdateTable('IATA_airports', {'code': 'text nn u',
##                                      'name': 'text nn',
##                                      'nameU': 'text nn'}, Airs)
##    else: # ошибка!
##        print(mAir)

    # База городов IATA
##    mAir = IATA.GetCity()
##    if mAir[0] != '#':
##        Airs = []
##        for air in mAir:
##            mRow = []
##            mRow.append(air['code'])
##            mRow.append(air['name'])
##            mRow.append(air['name'].upper().replace('Ё','Е'))
##            Airs.append(mRow)
##        UpdateTable('IATA_cities', {'code': 'text nn u',
##                                      'name': 'text nn',
##                                      'nameU': 'text nn'}, Airs)
##    else: # ошибка!
##        print(mAir)

    # База стран IATA
    mAir = IATA.GetCountry()
    if mAir[0] != '#':
        Airs = []
        for air in mAir:
            mRow = []
            mRow.append(air['code'])
            mRow.append(air['code3'])
            mRow.append(air['iso_numeric'])
            mRow.append(air['name'])
            mRow.append(air['name'].upper().replace('Ё','Е'))
            Airs.append(mRow)
        UpdateTable('IATA_countries', {'code': 'text nn u', 'code3': 'text nn',
                                    'iso': 'text', 'name': 'text nn',
                                      'nameU': 'text nn'}, Airs)
    else: # ошибка!
        print(mAir)
