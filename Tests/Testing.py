# -*- coding: utf-8 -*-
# Процессы тестирования сервисов/функций и самого бота
import Fixer

Tests = []  # Хранилище всех тестов
TestsDef = {}  # Хранилище всех функций для тестирования

# Все виды сравнения возвращают значение от 0 до 1
# (от полного несовпадения, до полного совпадения)


# Сравнение с эталонным (для строк)
def strEqual(stest, setalon):
    if stest == setalon:
        return 1
    else:
        if stest.strip() == setalon.strip():
            return 0.95
        if stest.strip().upper() == setalon.strip().upper():
            return 0.9
    return 0


# Сравнение с эталонным (float)
def fEqual(ftest, fetalon):
    if ftest == fetalon:
        return 1
    else:
        if abs(ftest - fetalon) / fetalon > 0.01:
            return 0
        else:
            return 1 - abs(ftest - fetalon) / (fetalon * 0.01)


# Сравнение с эталонным (для массивов)
def listEqual(mtest, metalon):
    if mtest == metalon: return 1
    if mtest == []: return 0 
    rez = 0
    fl = 1 / len(mtest)
    i = 0
    for item in mtest:
        if i < len(metalon):
            if item == metalon[i]: rez += fl
        else:
            et = 0
            for ietalon in metalon:
                if item == ietalon:
                    rez += fl * abs(et-i)/len(metalon)
                elif isinstance(item, str) and isinstance(ietalon, str):
                    rez += strEqual(item, ietalon) * fl * abs(et-i)/len(metalon)
                elif isinstance(item, float) and isinstance(ietalon, float):
                    rez += fEqual(item, ietalon) * fl * abs(et-i)/len(metalon)
            et += 1
        i += 1
    return rez


# Класс сравнения - compare
class Comp:
    # Проверка на работоспособность
    def isWork(test, *notwork):
        for iwork in notwork:
            if test == iwork:
                return 0
        return 1

    # Проверка на работоспособность (для строкового ответа)
    def sWork(test):
        try:
            bug, text = Fixer.strfind(test, ['#bug:','#problem:','#err:','#critical:'])
            if bug != '':
                return 0
            return 1
        except Exception as e:
            Fixer.errlog('Testing.sWork', str(e))
            return 0

    # Сравнение по типу значений
    def isType(testvalue, etalonvalue):
        if type(testvalue) == type(etalonvalue):
            return 1
        else:
            return 0
    
    # Сравнение с эталонным
    def Equal(test, etalon):
        if test == etalon:
            return 1
        else:
            return 0

    # Сравнение с эталонным (float)
    def fEqual(ftest, fetalon):
        try:
            return fEqual(ftest, fetalon)
        except Exception as e:
            Fixer.errlog('Testing.fEqual', str(e))
            return 0

    # Сравнение с эталонным (для строк)
    def strEqual(stest, setalon):
        try:
            from Services.StrMorph import String, Word
            if strEqual(stest, setalon) != 0:
                return strEqual(stest, setalon)
            else:
                if stest.strip() == '': return 0.0
                rez = 0.0
                scount = String.StringsCount(setalon)
                fl = 0.9 / scount
                i = 0
                for istr in String.GetStrings(stest):
                    if i < scount:
                        stret = String.GetStrings(setalon)[i]
                        if strEqual(istr, stret) >= 0.9: rez += fl * strEqual(istr, stret)
                    else:
                        et = 0
                        for ietalon in String.GetStrings(setalon):
                            if strEqual(istr, stret) >= 0.9: rez += fl * strEqual(istr, stret) * abs(et-i)/scount
                            elif String.WordsCount(istr) > 1 and String.WordsCount(ietalon) > 1:
                                rez += fl * listEqual(String.GetWords(istr), String.GetWords(ietalon)) * 0.9
                            et += 1
                    i += 1
                return rez
        except Exception as e:
            Fixer.errlog('Testing.strEqual', str(e))
            return 0.0

    # Сравнение с эталонным (для массивов)
    def listEqual(mtest, metalon):
        return listEqual(mtest, metalon)

# Процесс тестирования
class Test:
    # Добавление теста
    def Add(nameservice, service, name, testvalue, etalonvalue, time=0, critery=1):
        print(service, TestsDef)
        if service in TestsDef:
            TestsDef[service]['test'] = True
            TestsDef[service]['tests'].append(name)
        iTest = []
        iTest.append(service)  # 0
        iTest.append(name)  # 1
        iTest.append(str(testvalue).replace('\n', '\\n'))  # 2
        iTest.append(str(etalonvalue).replace('\n', '\\n'))  # 3
        ftest = 0; comm = ''
        if type(testvalue) == type(etalonvalue):  # если совпадают типы
            comm = 'Сравнение ' + str(type(testvalue))
            if isinstance(testvalue, str) and isinstance(etalonvalue, str):  # если на входе строки
                ftest = Comp.strEqual(testvalue, etalonvalue)
            elif isinstance(testvalue, float) and isinstance(etalonvalue, float):  # если на входе float
                ftest = Comp.fEqual(testvalue, etalonvalue)
            elif isinstance(testvalue, list) and isinstance(etalonvalue, list):  # если на входе list
                ftest = Comp.listEqual(testvalue, etalonvalue)
            else: # если на входе всё что угодно
                ftest = Comp.Equal(testvalue, etalonvalue)
        else: ftest = 0; comm ='Разные типы!'  # если типы не совпадают
        iTest.append(ftest)  # 4
        if ftest >= critery:
            iTest.append(True)  # 5
        else:
            iTest.append(False)  # 5
        iTest.append(time)  # 6
        iTest.append(comm)  # 7
        Tests.append(iTest)  # добавление теста
        return iTest

    # Добавление прочих тестов: iswork, swork, istype
    def AddSimple(nameservice, service, name, testvalue, testtype='iswork', time=0, criteries=[]):
        if service in TestsDef:
            TestsDef[service]['test'] = True
            TestsDef[service]['tests'].append(name)
        iTest = []
        iTest.append(service) # 0 
        iTest.append(name) # 1
        iTest.append(str(testvalue)) # 2
        iTest.append(str(criteries)) # 3
        testtype = testtype.lower().strip()
        ftest = 0; comm = 'Проверка ' + testtype
        if testtype == 'istype':
            ftest = Comp.isType(testvalue, criteries)
        elif testtype == 'swork':
            ftest = Comp.sWork(testvalue)
        else: #iswork
            ftest = Comp.isWork(testvalue, *criteries) 
        iTest.append(ftest) # 4
        if ftest == 1: iTest.append(True) # 5
        else: iTest.append(False)
        iTest.append(time)  # 6
        iTest.append(comm)  # 7
        iTest.append(nameservice) # 8
        Tests.append(iTest) # добавление теста
        return iTest

    # Добавление функции для тестирования
    def AddDef(name):
        if name not in TestsDef:
            TestsDef[name] = {'test': False, 'tests': []}
            return True
        else:
            return False

# Класс отчёта
class Report:

    # Универсальный отчёт по сравнению
    def Write(item=-1):
        iTest = Tests[item]
        srep = '- NO!!!'
        if iTest[5]:
            srep = '+ OK!'
        fl = '{:.3f}'.format(iTest[4])
        #ms = '{:.3f}'.format(iTest[6])
        s = '%s : %s {%s} - %s: %s: "%s" = "%s"' % (srep, fl, iTest[0], iTest[1], iTest[7], iTest[2], iTest[3])
        return s

    # Универсальный отчёт по сравнению
    def WriteAll(items=0):
        mreport = []
        for i in range(0, len(Tests)):
            mreport.append(Report.Write(i))
        if items == 0:
            items = len(Tests)
        return Fixer.strFormat(mreport, items)

    # Универсальный отчёт по сравнению
    def WriteFails(items=0):
        mreport = []
        for i in range(0, len(Tests)):
            if Tests[i][5] == False:
                mreport.append(Report.Write(i))
        for test in TestsDef:
            if TestsDef[test]['test'] == False:
                mreport.append('- NOT! Не протестирована функция ' + test)
        if items == 0:
            items = len(mreport)
        return Fixer.strFormat(mreport, items, sobj='ошибок')
    
