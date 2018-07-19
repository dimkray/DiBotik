# -*- coding: utf-8 -*-
# IATA
# Key f09869c0-33d9-4f10-8fe3-5467b99492f7
# https://iatacodes.org/api/VERSION/ENDPOINT?api_key=YOUR-API-KEY&lang=ru

import Fixer
import config
import json
from Services.URLParser import URL
from DB.SQLite import Finder

api = 'https://iatacodes.org/api/v6/'
params = {'api_key': config.IATA_key, 'lang': 'ru'}

# Получение данных по коду/имени
def GetData(stype, code, name, db=True):
    colsReturn = ['code', 'name', 'cityName', 'timeZone', 'country', 'lat', 'lon',
                 'runwayLength', 'runwayElevation', 'phone', 'email', 'website']
    jair = {}; air = []
    if code != '':
        if db:
            if stype == 'cities':
                city = Finder.Find('IATA_cities', ['code'], code, ['code','name'])
                if len(city) > 0:
                    city = city[1] + ' '
                    air = Finder.FindAll('IATA_airports', ['cityNameU'], city, colsReturn)
            else:
                air = Finder.FindAll('IATA_airports', ['code'], code, colsReturn)
        else: jair = URL.GetData(api+stype, code, 'code', params=params, bjson=True)
    elif name != '':
        sname = 'nameU'
        if stype == 'cities': sname = 'cityNameU'
        if db: air = Finder.FindAll('IATA_airports', [sname], name, colsReturn)
    elif db == False:
        jair = URL.GetData(api+stype, params=params, bjson=True)
    if len(air) > 0 and code != '': return Fixer.Sort(air,0)
    if len(air) > 0 and name != '': return Fixer.Sort(air,1)
    if jair is None: return '#problem: null result'
    if 'response' in jair:
        air = jair['response']
        if len(air) == 1: return air[0]
        elif len(air) > 1: return air
        else: return {}
    else:
        if db: return air
        else: return jair
    

# Основной класс
class IATA:
    # Код Аэропорта
    def GetAirport(code=''):
        name = ''
        return GetData('airports', code, name, db=False)

    def Airport(code='', name=''):
        if code == name == '': return []
        return GetData('airports', code, name, db=True)
    
    # Код Города
    def GetCity(code=''):
        name = ''
        return GetData('cities', code, name, db=False)

    def City(code='', name=''):
        if code == name == '': return []
        return GetData('cities', code, name, db=True)

    # Код страны
    def GetCountry(code=''):
        jair = URL.GetData(api+'countries', code, 'code', params=params, bjson=True)
        if jair is None: return '#problem: null result'
        if 'response' in jair:
            air = jair['response']
            if len(air) == 1: return air[0]
            elif len(air) > 1: return air
            else: return {}
        else:
            return jair

    def Country(code='', name=''):
        scode = 'code'; query = code
        if code != '':
            if len(code) == 3: scode = 'code3'
        elif name != '':
            scode = 'nameU'; query = name
        else: return []
        air = Finder.FindAll('IATA_countries', [scode], query, ['code','code3','iso','name'])
        return air
