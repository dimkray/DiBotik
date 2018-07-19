# -*- coding: utf-8 -*-
# Сервис прогноза погоды
import requests
import Fixer
import config

# основной класс
class Weather:
    # поиск локации
    def GetLocation(x, y):
        try:
            m = []
            http = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
            payload = {'apikey': config.Weather_key, 'q': str(y) + ',' + str(x), 'language': 'ru-ru', 'details': 'true'} 
            r = requests.get(http, params=payload)
            if r.status_code == requests.codes.ok:      
                data = r.json()
                m.append(data['Key'])                                   # 0 - key
                m.append(data['Type'])                                  # 1 - Type
                m.append(data['LocalizedName'])                         # 2 - Название
                m.append(data['AdministrativeArea']['LocalizedName'])   # 3 - Район/область
                m.append( data['Country']['LocalizedName'])             # 4 - Страна
                m.append(str(data['TimeZone']['GmtOffset']))            # 5 - Часовой пояс
                if 'Value' in data['GeoPosition']['Elevation']['Metric']:
                    m.append(data['GeoPosition']['Elevation']['Metric']['Value']) # 6 - Высота над уровнем моря
                else:
                    m.append(0)
                if 'Population' in data['Details']:
                    m.append(data['Details']['Population'])             # 7 - Население региона
                else:
                    m.append(0)
                return m
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                m.append('#problem: '+ str(r.status_code))
                return m
        except Exception as e:
            Fixer.errlog('Weather.GetLocation', str(e))
            return '#bug: ' + str(e) 
    
    def Forecast(x, y, edate='0'):
        try:
            from datetime import date, datetime, timedelta
            s = ''
            edate = edate.upper()
            if edate == '0' or edate == 'СЕЙЧАС' or edate == 'СЕГОДНЯ' or edate == str(date.today()):
                s = 'Погода сегодня: '
                edate = str(date.today())
            elif edate == 'ЗАВТРА' or edate == str(date.today() + timedelta(days=1)):
                s = 'Прогноз погоды на завтра: '
                edate = str(date.today() + timedelta(days=1))
            elif edate == 'ПОСЛЕЗАВТРА' or edate == str(date.today() + timedelta(days=2)):
                s = 'Прогноз погоды на послезавтра: '
                edate = str(date.today() + timedelta(days=2))
            else:
                s = 'Прогноз погоды на ' + edate + ': '
            print(edate)
            # определение локации
            m = Weather.GetLocation(x,y)
            s += m[2] +' ['+m[1]+'] '+m[3]+' ('+m[4]+')\n'
            # прогноз погоды
            http = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + m[0]
            payload = {'apikey': config.Weather_key, 'language': 'ru-ru', 'details': 'true', 'metric': 'true'} 
            r = requests.get(http, params=payload)
            m = []
            if r.status_code == requests.codes.ok:
                data = r.json()
                Fixer.htext = data['Headline']['Link']
                for day in data['DailyForecasts']:
                    if day['Date'].find(edate) >= 0:
                        rsun = day['Sun']['Rise']
                        ssun = day['Sun']['Set']
                        poz = rsun.find('T')+1
                        poz2 = rsun.find('+')
                        s += 'Восход солнца: ' + rsun[poz:poz2] + '\n'
                        m.append(rsun[poz:poz2]) # 0 восход солнца
                        s += 'Заход солнца: ' + ssun[poz:poz2]
                        m.append(ssun[poz:poz2]) # 1 заход солнца
                        s1 = 'Прогноз погоды днём:\n'
                        d = day['Temperature']['Maximum']['Value']
                        if d > 0: ss = '+' 
                        else: ss = ''
                        s1 += 'Температура максимум: ' + ss + str(d) + 'º\n'
                        m.append(ss + str(d) + 'º') # 2 температура днём
                        s1 += 'Описание погоды: ' + day['Day']['LongPhrase'] + ' - вероятность осадков ' + str(day['Day']['PrecipitationProbability']) + '%\n'
                        m.append(day['Day']['LongPhrase']) # 3 описание погоды
                        m.append(str(day['Day']['PrecipitationProbability']) + '%') # 4 вероятность осадков
                        s1 += 'Объём осадков: ' + str(day['Day']['TotalLiquid']['Value']) + ' мм\n'
                        m.append(str(day['Day']['TotalLiquid']['Value']) + ' мм') # 5 объём осадков
                        s1 += 'Продолжительность осадков: ' + str(day['Day']['HoursOfPrecipitation']) + ' ч\n'
                        m.append(str(day['Day']['HoursOfPrecipitation']) + ' ч') # 6 Продолжительность осадков
                        s1 += 'Облачность: ' + str(day['Day']['CloudCover']) + '%\n'
                        m.append(str(day['Day']['CloudCover']) + '%') # 7 Облачность
                        s1 += 'Ветер: ' + str(day['Day']['Wind']['Speed']['Value']) + ' км/ч - направление ' + day['Day']['Wind']['Direction']['Localized'] + '\n'
                        m.append(str(day['Day']['Wind']['Speed']['Value']) + ' км/ч - направление ' + day['Day']['Wind']['Direction']['Localized']) # 8 Ветер
                        s1 += 'Солнечные часы: ' + str(day['HoursOfSun'])
                        m.append(str(day['HoursOfSun']) + ' ч.') # 9 Солнечные часы
                        s2 = 'Прогноз погоды ночью:\n'
                        d = day['Temperature']['Minimum']['Value']
                        if d > 0: ss = '+' 
                        else: ss = ''
                        s2 += 'Температура минимум: ' + ss + str(d) + 'º\n'
                        m.append(ss + str(d) + 'º') # 10 температура ночью
                        s2 += 'Описание погоды: ' + day['Night']['LongPhrase'] + ' - вероятность осадков ' + str(day['Night']['PrecipitationProbability']) + '%\n'
                        m.append(day['Night']['LongPhrase']) # 11 описание погоды
                        m.append(str(day['Night']['PrecipitationProbability']) + '%') # 12 вероятность осадков
                        s2 += 'Объём осадков: ' + str(day['Night']['TotalLiquid']['Value']) + ' мм\n'
                        m.append(str(day['Night']['TotalLiquid']['Value']) + ' мм') # 13 объём осадков
                        s2 += 'Продолжительность осадков: ' + str(day['Night']['HoursOfPrecipitation']) + ' ч\n'
                        m.append(str(day['Night']['HoursOfPrecipitation']) + ' ч') # 14 Продолжительность осадков
                        s2 += 'Облачность: ' + str(day['Night']['CloudCover']) + '%\n'
                        m.append(str(day['Night']['CloudCover']) + '%') # 15 Облачность
                        s2 += 'Ветер: ' + str(day['Night']['Wind']['Speed']['Value']) + ' км/ч - направление ' + day['Night']['Wind']['Direction']['Localized'] + '\n'
                        m.append(str(day['Night']['Wind']['Speed']['Value']) + ' км/ч - направление ' + day['Night']['Wind']['Direction']['Localized']) # 16 Ветер
                        m.append(s) # 17 Общая информация
                        m.append(s1) # 18 День
                        m.append(s2) # 19 Ночь
                if m == []: return '#problem: нет данных о погоде или не правильно указан запрос'
                return m
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                return '#problem: '+ str(r.status_code)
        except Exception as e:
            Fixer.errlog('Weather.Forecast', str(e))
            return '#bug: ' + str(e) 
