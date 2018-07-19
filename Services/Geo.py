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
    Fixer.log('Geo.Geolocator')
    try:
        return GoogleV3(api_key=config.GMaps_key, timeout=1)
    except Exception as e:
        Fixer.errlog('Geo.Geolocator', str(e))
        return '#bug: ' + str(e)

# Измерение расстояние от одной точки до другой (по глобальным координатам)
class Geo:
    def Distance(x1,y1,x2,y2):
        Fixer.log('Geo.Distance')
        try:
            dist = great_circle((x1, y1),(x2, y2))
            sdist = str(dist)
            return float(sdist[:sdist.find(' ')])
        except Exception as e:
            Fixer.errlog('Geo.Distance', str(e))
            return '#bug: ' + str(e)
    
    # поиск полного адреса и координат по отношению к локальной позиции пользователя
    def FullAddress(address):
        Fixer.log('Geo.FullAddress')
        try:
            location = Geolocator().geocode(address, exactly_one=True,
                timeout=5, region=None,
                components=None, language='ru', sensor=True)
            return '%s (%f, %f)' % (location.address, location.latitude, location.longitude)
        except Exception as e:
            Fixer.errlog('Geo.FullAddress', str(e))
            return '#bug: ' + str(e)

    # получение координат по адресу
    def GetCoordinates(address):
        Fixer.log('Geo.GetCoordinates')
        try:
            location = Geolocator().geocode(address, exactly_one=True,
                                timeout=5, language='ru', sensor=True)
            return (location.longitude, location.latitude)
        except Exception as e:
            Fixer.errlog('Geo.GetCoordinates', str(e))
            return (0, 0)  

    # получение координат одной строкой
    def Coordinates(address):
        Fixer.log('Geo.Coordinates')
        try:
            location = Geolocator().geocode(address, exactly_one=True,
                                timeout=5, language='ru', sensor=True)
            return '%f, %f' % (location.latitude, location.longitude)
        except Exception as e:
            Fixer.errlog('Geo.Coordinates', str(e))
            return '#bug: ' + str(e)

    # Получение адреса по координатам: X, Y
    def GetAddress(xlat,ylon):
        Fixer.log('Geo.GetAddress')
        try:
            location = Geolocator().reverse(str(xlat)+', '+str(ylon),
                                        exactly_one=True, timeout=5,
                                        language='ru', sensor=True)
            return location.address
        except Exception as e:
            Fixer.errlog('Geo.GetAddress!', str(e))
            return '#bug: ' + str(e)

    # получение координат по адресу (можно использовать Google или Yandex) - без использования токена!
    def GetLocation(FullAddress, bgoogle=True):
        Fixer.log('Geo.GetLocation')
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
            Fixer.errlog('Geo.GetLocation!', str(e))
            return '#bug: ' + str(e)

    # Получение часового пояса по координатам
    def GetTimezone(xlat,ylon):
        Fixer.log('Geo.GetTimezone')
        try:
            timezone = Geolocator().timezone(str(xlat)+', '+str(ylon))
            return str(timezone)
        except Exception as e:
            Fixer.errlog('Geo.GetTimezone!', str(e))
            return '#bug: ' + str(e)
