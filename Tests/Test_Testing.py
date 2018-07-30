from Profiler import Profiler
from Tests.Testing import Comp, Test, Report

service = 'Testing'

# здесь тестовая обработка #
with Profiler() as p:
    # isWork
    test = Comp.isWork(None, None)
    Test.Add(service, service + '.isWork', 'автопроверка', test, 0)

    test = Comp.isWork(1, None)
    Test.Add(service, service + '.isWork', 'автопроверка', test, 1)

    test = Comp.isWork('Работает', None, ['Работает'], 1, 'работает', {'Работает': 'Работает'})
    Test.Add(service, service + '.isWork', 'автопроверка', test, 1)

    test = Comp.isWork('Работает', None, ['Работает'], 1, u'Работает', {'Работает': 'Работает'})
    Test.Add(service, service + '.isWork', 'автопроверка', test, 0)

    # sWork
    test = Comp.sWork('Всё хорошо!')
    Test.Add(service, service + '.sWork', 'автопроверка', test, 1)

    test = Comp.sWork('#bug: Всё плохо :(')
    Test.Add(service, service + '.sWork', 'автопроверка', test, 0)

    test = Comp.sWork('#critical: Всё ужасно :(')
    Test.Add(service, service + '.sWork', 'автопроверка', test, 0)

    test = Comp.sWork('#probem Всё не так плохо :)')
    Test.Add(service, service + '.sWork', 'автопроверка', test, 1)

    test = Comp.sWork(['Другой тип'])
    Test.Add(service, service + '.sWork', 'автопроверка', test, 0)

    # isType
    test = Comp.isType(1, 100)
    Test.Add(service, service + '.isType', 'автопроверка', test, 1)

    test = Comp.isType(5.0, 5)
    Test.Add(service, service + '.isType', 'автопроверка', test, 0)

    test = Comp.isType({}, [])
    Test.Add(service, service + '.isType', 'автопроверка', test, 0)

    test = Comp.isType('строка', "другая строка")
    Test.Add(service, service + '.isType', 'автопроверка', test, 1)

    # Equal
    test = Comp.Equal(100, 99)
    Test.Add(service, service + '.Equal', 'автопроверка', test, 0)

    test = Comp.Equal(5.0, 5)
    Test.Add(service, service + '.Equal', 'автопроверка', test, 1)

    test = Comp.Equal({'тест': 'тест'}, ['тест'])
    Test.Add(service, service + '.Equal', 'автопроверка', test, 0)

    test = Comp.Equal('строка', "строка")
    Test.Add(service, service + '.Equal', 'автопроверка', test, 1)

    test = Comp.Equal('строка2', u'строка2')
    Test.Add(service, service + '.Equal', 'автопроверка', test, 1)

    test = Comp.Equal('строка2', 'строка 2')
    Test.Add(service, service + '.Equal', 'автопроверка', test, 0)

    test = Comp.Equal(['тест1'], ['тест'])
    Test.Add(service, service + '.Equal', 'автопроверка', test, 0)

    test = Comp.Equal(['тест', 'тест2'], ['тест'])
    Test.Add(service, service + '.Equal', 'автопроверка', test, 0)

    # fEqual
    test = Comp.fEqual('строка2', 'строка2 ')
    Test.Add(service, service + '.fEqual', 'автопроверка', test, 0)

    test = Comp.fEqual(1, 2)
    Test.Add(service, service + '.fEqual', 'автопроверка', test, 0)

    test = Comp.fEqual(1.000, 0.995)
    Test.Add(service, service + '.fEqual', 'автопроверка', test, 0.5, critery=0.49)

    test = Comp.fEqual(0.0001, 0)
    Test.Add(service, service + '.fEqual', 'автопроверка', test, 0)

    test = Comp.fEqual(0.998, 0.998)
    Test.Add(service, service + '.fEqual', 'автопроверка', test, 1)

    test = Comp.fEqual(1, '1')
    Test.Add(service, service + '.fEqual', 'автопроверка', test, 0)

    # strEqual
    test = Comp.strEqual(' тест', 'тест')
    Test.Add(service, service + '.strEqual', 'автопроверка', test, 0.95)
    
    test = Comp.strEqual('Тест', 'тест')
    Test.Add(service, service + '.strEqual', 'автопроверка', test, 0.9)
    
    test = Comp.strEqual('тест', 'тест')
    Test.Add(service, service + '.strEqual', 'автопроверка', test, 1)

    test = Comp.strEqual(1, 'тест')
    Test.Add(service, service + '.strEqual', 'автопроверка', test, 0.0)

    # доработать...
    test = Comp.strEqual('тест тестов', 'тестов тест')
    Test.Add(service, service + '.strEqual', 'автопроверка', test, 0.0)
    
    test = Comp.strEqual('Предложение один. Предложение два', 'Предложение два. Предложение один')
    Test.Add(service, service + '.strEqual', 'автопроверка', test, 0.0)
    
    test = Comp.strEqual('слово дело слово дело', 'слово делать')
    Test.Add(service, service + '.strEqual', 'автопроверка', test, 0.0)

    test = Comp.strEqual('Квартира в центре Петербурга со скидкой 20%! Дом сдан!',
                         'Квартира в центре Петербурга со скидкой 25%! Дом сдан!')
    Test.Add(service, service + '.strEqual', 'автопроверка', test, 0.45)

    # listEqual
    test = Comp.listEqual('тесты', 'тест')
    Test.Add(service, service + '.listEqual', 'автопроверка', test, 0.8)
    
    test = Comp.listEqual([1, 2, 3, 4, 5], [1, 2, 3, 5, 4])
    Test.Add(service, service + '.listEqual', 'автопроверка', test, 0.6, critery=0.9)
    
    test = Comp.listEqual(['1', '2', '6'], ['1', '2', '3'])
    Test.Add(service, service + '.listEqual', 'автопроверка', test, 0.666, critery=0.8)

    test = Comp.listEqual([1, 2, 3, 4.1, 5], [1, 2, 3, 4.101, 5])
    Test.Add(service, service + '.listEqual', 'автопроверка', test, 0.8)

    # Add
    test = Test.Add(service, 'Test', 'Name', 'test', 'Test', critery=0.9)
    Test.Add(service, service+'.Add', 'автопроверка', test, ['Test', 'Name', 'test', 'Test', 0.9, True, 0, "Сравнение <class 'str'>"])

print('------- Запущены тесты --------')
print(Report.WriteAll())
print('')
print('------- Найдены ошибки --------')
print(Report.WriteFails())
