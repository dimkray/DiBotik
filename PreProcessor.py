# -*- coding: utf-8 -*-
# ПреПроцессор - стартовый обработчик пользовательских запросов
import Fixer
from Services.Yandex import Ya
from Services.Analyzer import TextFinder
from Services.StrMorph import String, Word

# мультипроцессор, препроцессорная обработка, препроцессорное автоопределение сервиса
# возвращаемый формат: [[текст для процессора],[предполагаемый сервис]]
def MultiProcessor(text):
    Fixer.log('PreProcessor.MultiProcessor')
    # происк мультизапроса и выполнение запроса (анализ)
    mMulti = String.GetStrings(text)
    mDel = []; i = 0
    for item in mMulti:  # поиск пустых запросов
        if item.strip() == '':
            mDel.append(i)
        i += 1
    for iDel in mDel:  # удаление пустых запросов
        del(mMulti[iDel])
    return mMulti


# препроцессорный обработчик пользовательских запросов
def ReadMessage(text):
    Fixer.log('PreProcessor.ReadMessage', text)
    # Фиксация слов
    fix = ''
    text = Fixer.strSpec(text)
    if '"' in text:
        fix_start = text.find('"')
        fix_end = text.find('"', fix_start+1)
        if fix_end > 0:
            no_fix = text[:fix_start] + '["]' + text[fix_end+1:]
        else:
            no_fix = text[:fix_start] + '["]'
        fix = text[fix_start+1:fix_end]
        text = no_fix
    # Запуск сервиса Яндекс.Спеллер для исправления пользовательских опечаток
    text = Ya.Speller(text)
    Fixer.log('Яндекс.Спеллер: ' + text)
    stext = text.upper()
    stext = stext.replace('Ё', 'Е')
    # Возвращаем зафиксированные слова
    stext = stext.replace('["]', fix)
    # Поиск совпадений по первому слову
    Fixer.log('PreProcessor.Word1')
    for word in Fixer.Word1:
        if word == stext[0:len(word)]:
            poz = len(word)
            text = Fixer.Word1[word] + text[poz:] # убираем первое слово - добавляем сервис #
            Fixer.log('PreProcessor.Word1', 'Найдено совпадение по первому слову: ' + text)
            break
    # Поиск совпадений по ключевым словам
    Fixer.log('PreProcessor.KeyWord')
    if Fixer.bAI:
        for word in Fixer.KeyWord:
            ktext = text.upper()
            if ktext.find(word) >= 0:
                text = Fixer.KeyWord[word] + text # добавляем сервис #
                Fixer.log('PreProcessor.KeyWord', 'Найдено совпадение по ключевому слову [' + word + ']:' + text)
                break
    # Анализ сообщения
    if ': ' not in text:
        Fixer.log('PreProcessor.Analyzer')
        texttype, count = TextFinder.AnalyzeType(text)
        if texttype == 50 and count > 3: text = '#translate: русский: ' + text
        if texttype == 40 and count > 1: text = '#calculator: ' + text
    if text[0] == '#': Fixer.bAI = False # отключаем искуственный интеллект
    return text
