# -*- coding: utf-8 -*-
# Простой сервис универсальных развлечений
import Fixer
from DB.SQLite import SQL, Finder

tb = 'anecdotes'

class Fun:
    # произвольный анекдот
    def Anecdote(iType = -1):
        import random
        try:
            random.seed()
            if iType == -1: # тип анекдота - все виды
                ilen = SQL.Count(tb)
                i = random.randint(0, ilen-1)
                return SQL.ReadValue(tb, 'id', i, 'text')
            else: # тип анекдота - особый
                m = SQL.ReadValues(tb, 'type', iType, 'text')
                i = random.randint(0, len(m)-1)
                return m[i]
        except Exception as e:
            Fixer.errlog('Fun.Anecdote', str(e))
            return '#bug: ' + str(e)

    # поиск анекдота
    def FindAnecdote(text):
        try:
            return Finder.strFind(tb, ['textU'], text, ['text'])
        except Exception as e:
            Fixer.errlog('Fun.FindAnecdote', str(e))
            return '#bug: ' + str(e)

    # добавление анекдота в базу
    def AddAnecdote(text, iType = 0):
        try:
            ilen = SQL.Count(tb)
            s = SQL.WriteRow(tb, [ilen, iType, text, text.upper()])
            if s == 'OK': return 'Анекдот успешно добавлен в базу :)'
            else: return s
        except Exception as e:
            Fixer.errlog('Fun.AddAnecdote', str(e))
            return '#bug: ' + str(e) 
