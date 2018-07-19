# -*- coding: utf-8 -*-
# Сервис по работе с базами данных (wrapper)

import Fixer
from DB.SQLite import SQL, CSV

tDel = [] # Список удалённых таблиц
items = 100000; block = 1000000 # размер блока

class Worker:
    mTableCSV = [] # Шапка таблицы CSV (временная)
    mDataCSV = [] # Временные данные таблицы
    
    # Добавление новой таблицы или добавление данных в таблицу
    def AddTable(NameTable, dCols, data):
        print('Создание таблицы "%s"' % NameTable)
        print('Результат: ' + SQL.Table(NameTable, dCols))
        print('Запись данных: %i строк' % len(data))
        result = SQL.WriteBlock(NameTable, data)
        print('Результат: ' + result)
        print('-------------------------------------')
        return result

    # Удаление старой таблицы и формирование новой таблицы
    def UpdateTable(NameTable, dCols, data):
        if NameTable not in tDel: # проверяем не удалена ли таблица уже
            print('Удаление старой таблицы "%s"' % NameTable)
            print('Результат: ' + SQL.Delete(NameTable))
            print('Создание новой таблицы "%s"' % NameTable)
            print('Результат: ' + SQL.Table(NameTable, dCols))
            tDel.append(NameTable)
        print('Запись данных: %i строк' % len(data))
        result = SQL.WriteBlock(NameTable, data)
        print('Результат: ' + result)
        print('-------------------------------------')
        return result

    # Удаление старой таблицы и формирование новой таблицы (словарь)
    def UpdateTableDict(NameTable, dictData, dCols = {'id': 'text pk nn u', 'text': 'text'}):
        print('Удаление старой таблицы-словаря "%s"' % NameTable)
        print('Результат: ' + SQL.Delete(NameTable))
        print('Создание новой таблицы-словаря "%s"' % NameTable)
        print('Результат: ' + SQL.Table(NameTable, dCols))
        tDel.append(NameTable)
        print('Запись данных: %i строк' % len(dictData))
        result = SQL.WriteDictBlock(NameTable, dictData)
        print('Результат: ' + result)
        print('-------------------------------------')
        return result

    # Чтение данных CSV по блокам
    def ReadBlockCSV(csvFile, iblock=0, separator=';', symb='\\"', bRead=True):
        print('Чтение данных файла "%s" - блок %i' % (csvFile, iblock+1))
        if bRead:
            Worker.mDataCSV, mTable = CSV.Reader(csvFile, separator=separator,
                            items=block, istart=iblock*block, download=items, symb=symb)
        else:
            Worker.mDataCSV, mTable = CSV.AutoReader(csvFile, separator=separator,
                            items=block, istart=iblock*block, download=items, quotechar=symb)
        if mTable != []: Worker.mTableCSV = mTable
        print(Worker.mTableCSV)
        return len(Worker.mDataCSV) # возвращает число загруженных строк

    # Создание новой таблицы (с удалением старой) на основе таблицы CSV - по блокам
    # dCols - соотношение данных таблицы ДБ с шапкой таблицы CSV: {nameDB: nameCSV}
    def UpdateBlockCSV(NameTable, dCols, dColsCSV={}):
        indexes = [] # индексы CSV для записи данных в БД
        cols = dCols.keys() # названия полей таблицы БД
        if dColsCSV == {}:
            for col in cols:
                try:
                    i = Worker.mTableCSV.index(col) # поиск соотвествия таблицы
                except:
                    i = -1
                    print('!!! BUG - not found col "%s"' % col)
                    Fixer.log('UpdateBlockCSV', '!!! BUG - not found col "%s"' % col)
                indexes.append(i)
        else:
            for col in cols:
                if isinstance(dColsCSV[col], int):
                    indexes.append(dColsCSV[col])
                else:
                    try:
                        i = Worker.mTableCSV.index(dColsCSV[col]) # поиск индекса в dColsCSV
                    except:
                        i = -1
                        print('!!! BUG - not found col "%s"' % col)
                        Fixer.log('UpdateBlockCSV', '!!! BUG - not found col "%s"' % col)
                    indexes.append(i) 
        data = [] # временное хранилище данных
        print(indexes)
        for row in Worker.mDataCSV:
            try:
                m = []
                for i in indexes:
                    if i != -1: m.append(row[i])
                    else: m.append(None)
                data.append(m)
            except Exception as e:
                print('!!! BUG - ' + str(e))
                print(row)
                Fixer.log('UpdateBlockCSV', '!!! BUG - %s\n%s' % (str(e), str(row)))
        print('Обработано данных: %i строк' % len(data))
        print('-------------------------------------')
        result = Worker.UpdateTable(NameTable, dCols, data)
        return result

    # Создание новой таблицы (с удалением старой) на основе CSV-файла (для ЕГР)
    # dCols - соотношение данных таблицы ДБ с шапкой таблицы CSV: {nameDB: nameCSV}
    def UpdateTableCSV(csvFile, NameTable, dCols, dColsCSV={}, blocks=1, separator=';', symb='\\"'):
        for iblock in range(0, blocks): # обработка данных блоками
            print('Загружено данных: %i строк' % Worker.ReadBlockCSV(csvFile,
                                        iblock=iblock, separator=separator, symb=symb))
            result = Worker.UpdateBlockCSV(NameTable, dCols=dCols, dColsCSV=dColsCSV)
        return result

    # Индексация таблицы (по завершению загрузки данных в таблицу)
    def Indexation(NameTable, cols):
        print('Индексация полей таблицы "%s"' % NameTable)
        sql = 'CREATE INDEX %s ON %s (' % ( NameTable + '_idx', NameTable)
        for col in cols:
            sql += col + ', '
        sql = sql[:-2]
        sql += ')'
        result = SQL.sql(sql)
        print('Результат: ' + result)
        print('-------------------------------------')
        return result

    # Чтение файла в словарь
    def DictionaryCSV(csvFile, keycol='id', mCols=[], separator=';', symb='\\'):
        print('Чтение данных файла "%s" - в словарь' % csvFile)
        data, mlist = CSV.AutoReader(csvFile, separator=separator, quotechar=symb, download=items)
        indexes = [] # индексы CSV для записи данных в БД
        print(mlist)
        try:
            icol = mlist.index(keycol)
        except: icol = 0    
        if mCols != []:
            for col in mCols:
                try:
                    i = mlist.index(col) # поиск соотвествия таблицы
                except:
                    i = -1
                    print('!!! BUG - not found col "%s"' % col)
                    Fixer.log('DictionaryCSV', '!!! BUG - not found col "%s"' % col)
                indexes.append(i)
        elif icol == 0: indexes.append(1)
        else: indexes.append(0)
        print(indexes)
        dData = {} # Создание словаря
        for row in data:
            try:
                m = []
                if len(indexes) > 1:
                    for i in indexes:
                        if i != -1: m.append(row[i])
                        else: m.append(None)
                    dData[row[icol]] = m
                else:
                    dData[row[icol]] = row[indexes[0]]
            except Exception as e:
                print('!!! BUG - ' + str(e))
                print(row)
                Fixer.log('UpdateBlockCSV', '!!! BUG - %s\n%s' % (str(e), str(row)))
        print('Обработано данных: %i строк' % len(data))
        print('-------------------------------------')
        return dData # возвращение словаря

