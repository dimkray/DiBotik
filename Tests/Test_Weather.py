import requests
#import Services.Yandex
apikey = 'MsEJc54YAFZeJOumeXpehdfguhJMLK1R'

stest = input('Введите тестовые координаты: ')

# здесь тестовая обработка #

# поиск локации
http = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
payload = {'apikey': apikey, 'q': stest, 'language': 'ru-ru'} 
r = requests.get(http, params=payload)
if r.status_code == requests.codes.ok:      
    data = r.json()
    key = data['Key']
    print('Key: ' + data['Key'])
    print('Тип: ' + data['Type'])
    print('Название: ' + data['LocalizedName'])
    print('Район/область: ' + data['AdministrativeArea']['LocalizedName'])
    print('Страна: ' + data['Country']['LocalizedName'])
    print('Часовой пояс: ' + str(data['TimeZone']['GmtOffset']))
    print('Высота над уровнем моря: ' + str(data['GeoPosition']['Elevation']['Metric']['Value']))
else:
    # Если ошибка - то спец.сообщение с номером ошибки
    print('#problem: '+ str(r.status_code))

# прогноз погоды
http = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + key
payload = {'apikey': apikey, 'language': 'ru-ru', 'details': 'true', 'metric': 'true'} 
r = requests.get(http, params=payload)
if r.status_code == requests.codes.ok:
    data = r.json()
    print('link: ' + data['Headline']['Link'])
    day = data['DailyForecasts'][0]
    rsun = day['Sun']['Rise']
    ssun = day['Sun']['Set']
    poz = rsun.find('T')+1
    poz2 = rsun.find('+')
    print('Общий прогноз на ' + rsun[:poz-1])
    print('Восход солнца: ' + rsun[poz:poz2])
    print('Заход солнца: ' + ssun[poz:poz2])
    print('Прогноз погоды днём:')
    print('Температура: ' + str(day['Temperature']['Maximum']['Value']) + 'º')    
    print('Описание погоды: ' + day['Day']['LongPhrase'] + ' - вероятность осадков ' + str(day['Day']['PrecipitationProbability']) + '%')
    print('Объём осадков: ' + str(day['Day']['TotalLiquid']['Value']) + ' мм')
    print('Продолжительность осадков: ' + str(day['Day']['HoursOfPrecipitation']) + ' ч')
    print('Облачность: ' + str(day['Day']['CloudCover']) + '%')
    print('Ветер: ' + str(day['Day']['Wind']['Speed']['Value']) + ' км/ч - направление ' + day['Day']['Wind']['Direction']['Localized'])
    print('Солнечные часы: ' + str(day['HoursOfSun']))
    print('Прогноз погоды ночью:')
    print('Температура min: ' + str(day['Temperature']['Minimum']['Value']) + 'º')
    print('Описание погоды: ' + day['Night']['LongPhrase'] + ' - вероятность осадков ' + str(day['Night']['PrecipitationProbability']) + '%')
    print('Объём осадков: ' + str(day['Night']['TotalLiquid']['Value']) + ' мм')
    print('Облачность: ' + str(day['Day']['CloudCover']) + '%')
    print('Продолжительность осадков: ' + str(day['Night']['HoursOfPrecipitation']) + ' ч')
    print('Ветер: ' + str(day['Night']['Wind']['Speed']['Value']) + ' км/ч - направление ' + day['Night']['Wind']['Direction']['Localized'])
    
else:
    # Если ошибка - то спец.сообщение с номером ошибки
    print('#problem: '+ str(r.status_code))


import time; time.sleep(5)
