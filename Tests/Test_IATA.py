from Profiler import Profiler
from Tests.Testing import Test, Report
from Services.IATA import IATA

service = 'IATA'

print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #
with Profiler() as p:
    # Airport
    test = IATA.GetAirport(code='ACM')
    Test.Add(service, service+'.GetAirport','normal code',
             test, {'code': 'ACM', 'name': 'Арика'})

    test = IATA.GetAirport(code='AR')
    Test.Add(service, service+'.GetAirport','unreal code',
             test, {})

    test = IATA.Airport(code='ACM')
    etalon = [('ACM', 'Арика', 'Арика', 5.0, 'Колумбия', -2.133, -71.783, '', '', '', '', '')]
    Test.Add(service, service+'.Airport','normal code db', test, etalon)

    test = IATA.Airport(code='ACM', name='Шереметьево')
    Test.Add(service, service+'.Airport','normal code-name db', test, etalon)

    test = IATA.Airport(name='Шереметьево')
    etalon = [('SVO', 'Шереметьево', 'Москва', 3.0, 'Россия',
               55.972642, 37.414589, 3700, 190, '+7 (495) 232 65 65', '', 'http://www.svo.aero')]
    Test.Add(service, service+'.Airport','normal name db', test, etalon)
    
    test = IATA.Airport(name='ьево')
    etalon = [('BQS', 'Игнатьево', 'Благовещенск', 9.0, 'Россия', 50.425394, 127.412478, '', 194, '', '', ''),
              ('SVO', 'Шереметьево', 'Москва', 3.0, 'Россия', 55.972642, 37.414589, 3700, 190,
               '+7 (495) 232 65 65', '', 'http://www.svo.aero')]
    Test.Add(service, service+'.Airport','normal name db', test, etalon)

    test = IATA.Airport(code='ACCN')
    Test.Add(service, service+'.Airport','unreal code db', test, [])

    test = IATA.Airport(name='Перьмь')
    Test.Add(service, service+'.Airport','unreal name db', test, [])

    test = IATA.Airport()
    Test.Add(service, service+'.Airport','crash db', test, [])

    # City
    test = IATA.GetCity(code='PEE')
    Test.Add(service, service+'.GetCity','normal code',
             test, {'code': 'PEE', 'country_code': 'RU', 'name': 'Пермь'})

    test = IATA.GetCity(code='EEE')
    Test.Add(service, service+'.GetCity','unreal code', test, {})

    test = IATA.City(code='PEE')
    etalon = [('PEE', 'Большое Савино', 'Пермь', -2.0, 'Россия',
               57.914517, 56.021214, 3200, 123, '+7 (342) 294-97-71',
               '', 'http://www.aviaperm.ru')]
    Test.Add(service, service+'.City','normal code db', test, etalon)

    test = IATA.City(code='PEE', name='Москва')
    Test.Add(service, service+'.City','normal code-name db', test, etalon)

    test = IATA.City(name='Екат')
    etalon = [('SVX', 'Кольцово', 'Екатеринбург', 5.0, 'Россия',
               56.743108, 60.802728, 3026, 233, '+7 (343) 264-42-02', '',
               'http://www.koltsovo.ru')]
    Test.Add(service, service+'.City','normal name db', test, etalon)

    test = IATA.City(name='Нью-Йорк') # 11 аэропортов
    Test.Add(service, service+'.City','normal name big db', len(test), 11)

    test = IATA.City(code='EEE')
    Test.Add(service, service+'.City','unreal code db', test, [])

    test = IATA.City(name='Перьмь')
    Test.Add(service, service+'.City','unreal name db', test, [])

    test = IATA.City()
    Test.Add(service, service+'.City','crash db', test, [])

    # Country
    test = IATA.GetCountry(code='RU')
    Test.Add(service, service+'.GetCountry','normal code',
             test, {'code': 'RU', 'code3': 'RUS', 'iso_numeric': 643, 'name': 'Россия', 'languages': []})

    test = IATA.GetCountry(code='RUU')
    Test.Add(service, service+'.GetCountry','unreal code', test, {})

    test = IATA.Country(code='RU')
    etalon = [('RU', 'RUS', '643', 'Россия')]
    Test.Add(service, service+'.Country','normal code db', test, etalon)

    test = IATA.Country(name='росс')
    Test.Add(service, service+'.Country','normal name db', test, etalon)

    test = IATA.Country(code='EST', name='Россия')
    Test.Add(service, service+'.Country','normal code-name db', test, [('EE', 'EST', '233', 'Эстония')])

    test = IATA.Country(code='WW')
    etalon = [('RU', 'RUS', '643', 'Россия')]
    Test.Add(service, service+'.Country','unreal code db', test, [])

    test = IATA.Country(name='еее')
    Test.Add(service, service+'.Country','unreal name db', test, [])

    test = IATA.Country()
    Test.Add(service, service+'.Country','crush db', test, [])


print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
