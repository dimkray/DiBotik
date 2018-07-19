# -*- coding: utf-8 -*-
# Сервис работы с координатами земли и приём/возврат адреса
import Fixer
import config
import json
from urllib.parse import quote_plus
from geopy.distance import great_circle
from geopy.geocoders import GoogleV3
from Services.URLParser import URL

# Локатор Google
def Geolocator():
    try:
        return GoogleV3(api_key=config.GMaps_key, timeout=1)
    except Exception as e:
        Fixer.errlog('Geolocator', str(e))
        return '#bug: ' + str(e)

# Измерение расстояние от одной точки до другой (по глобальным координатам)
class Geo:
    def Distance(x1,y1,x2,y2):
        try:
            dist = great_circle((x1, y1),(x2, y2))
            sdist = str(dist)
            return float(sdist[:sdist.find(' ')])
        except Exception as e:
            Fixer.errlog('Ошибка в Geo.Distance!: ' + str(e))
            return '#bug: ' + str(e)
    
    # поиск полного адреса и координат по отношению к локальной позиции пользователя
    def FullAddress(address):
        try:
            location = Geolocator().geocode(address, exactly_one=True,
                timeout=5, region=None,
                components=None, language='ru', sensor=True)
            return '%s (%f, %f)' % (location.address, location.latitude, location.longitude)
        except Exception as e:
            Fixer.errlog('Ошибка в Geo.FullAddress!: ' + str(e))
            return '#bug: ' + str(e)

    # получение координат по адресу
    def GetCoordinates(address):
        try:
            location = Geolocator().geocode(address, exactly_one=True,
                                timeout=5, language='ru', sensor=True)
            return (location.longitude, location.latitude)
        except Exception as e:
            Fixer.errlog('Ошибка в Geo.GetCoordinates!: ' + str(e))
            return (0, 0)  

    # получение координат одной строкой
    def Coordinates(address):
        try:
            location = Geolocator().geocode(address, exactly_one=True,
                                timeout=5, language='ru', sensor=True)
            return '%f, %f' % (location.latitude, location.longitude)
        except Exception as e:
            Fixer.errlog('Ошибка в Geo.Coordinates!: ' + str(e))
            return '#bug: ' + str(e)

    # Получение адреса по координатам: X, Y
    def GetAddress(xlat,ylon):
        try:
            location = Geolocator().reverse(str(xlat)+', '+str(ylon),
                                        exactly_one=True, timeout=5,
                                        language='ru', sensor=True)
            return location.address
        except Exception as e:
            Fixer.errlog('Ошибка в Geo.GetAddress!: ' + str(e))
            return '#bug: ' + str(e)

    # получение координат по адресу (можно использовать Google или Yandex) - без использования токена!
    def GetLocation(FullAddress, bgoogle=True):
        try:
            sGoogle = 'http://maps.google.com/maps/api/geocode/json?sensor=false&address='
            sYandex = 'http://geocode-maps.yandex.ru/1.x/?format=json&geocode='
            geoCodeURL = (sGoogle if bgoogle else sYandex) + quote_plus(FullAddress)
            data = URL.GetData(geoCodeURL)
            geoCodeJson = json.loads(data)
            if bgoogle: # Google
                status = geoCodeJson['status']
                if status.upper() == 'OK':
                    geoCodeLocation = geoCodeJson['results'][0]['geometry']['location']
                    return '%f, %f' % (geoCodeLocation['lat'], geoCodeLocation['lng'])
                else: return '#problem: ' + status
            else: # Yandex
                try:
                    geoCodeLocation = geoCodeJson['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                    poz = geoCodeLocation.find(' ')
                    lat = geoCodeLocation[:poz]
                    lng = geoCodeLocation[poz:]
                    return '%s, %s' % (lng, lat)
                except:
                    return '#problem: адрес не найден!'
        except Exception as e:
            Fixer.errlog('Ошибка в Geo.GetLocation!: ' + str(e))
            return '#bug: ' + str(e)

# тест
address = input('Напиши адрес: ')
print('Полный адрес: %s' % Geo.FullAddress(address))
Coords = Geo.GetCoordinates(address)
print(Coords[0])
print(Coords[1])
print('Координаты строкой: %s' % Geo.Coordinates(address))
print('Обратный адрес по координатам: %s' % Geo.GetAddress(Coords[1], Coords[0]))
print('Координаты строкой: ' + Geo.GetLocation(address, False))
