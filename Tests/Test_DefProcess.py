from Profiler import Profiler
from Tests.Testing import Test, Report
import DefProcess

service = 'DefProcess'

print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #
with Profiler() as p:
    # GetAllMembers
    test = DefProcess.GetAllMembers('self')
    etalon = ['__add__', '__class__', '__contains__', '__delattr__',
              '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
              '__getattribute__', '__getitem__', '__getnewargs__',
              '__gt__', '__hash__', '__init__', '__init_subclass__',
              '__iter__', '__le__', '__len__', '__lt__', '__mod__',
              '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
              '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__',
              '__str__', '__subclasshook__', 'capitalize', 'casefold',
              'center', 'count', 'encode', 'endswith', 'expandtabs',
              'find', 'format', 'format_map', 'index', 'isalnum',
              'isalpha', 'isdecimal', 'isdigit', 'isidentifier',
              'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle',
              'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans',
              'partition', 'replace', 'rfind', 'rindex', 'rjust',
              'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines',
              'startswith', 'strip', 'swapcase', 'title', 'translate',
              'upper', 'zfill']
    Test.Add(service + '.GetAllMembers', 'normal', test, etalon)

    # GetAllAttrs - пропуск, т.к. состав и порядок динамически меняется

    # GetGlobals
    test = DefProcess.GetGlobals()
    etalon = ['Fixer', 'inspect', 'Test', 'uniq', 'GetAllMembers',
              'GetAllAttrs', 'GetGlobals', 'GetClass', 'GetMembers',
              'GetAttrs', 'GetArgs', 'Code', 'Run']
    Test.Add(service + 'GetGlobals' , 'normal', test, etalon)

    # GetClass
    test = DefProcess.GetClass('Test')
    Test.Add(service + '.GetAllAttrs', 'normal', test, Test)

    # GetMembers
    test = DefProcess.GetMembers('Test')
    etalon = ['capitalize', 'casefold', 'center', 'count', 'encode',
              'endswith', 'expandtabs', 'find', 'format', 'format_map',
              'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit',
              'isidentifier', 'islower', 'isnumeric', 'isprintable',
              'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower',
              'lstrip', 'maketrans', 'partition', 'replace', 'rfind',
              'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split',
              'splitlines', 'startswith', 'strip', 'swapcase', 'title',
              'translate', 'upper', 'zfill']
    Test.Add(service + '.GetMembers', 'normal', test, etalon)

    # GetAttrs - пропуск, т.к. состав и порядок динамически меняется
    test = DefProcess.GetAttrs('Test')

    # GetArgs
    test = DefProcess.GetArgs(Test.Add)
    etalon = ['service', 'name', 'testvalue', 'etalonvalue', 'time', 'critery']
    Test.Add(service + '.GetArgs', 'normal', test, etalon)

    test = DefProcess.Code('4 + 2 / 5')
    Test.Add(service + '.GetArgs', 'normal 1', test, 4.4)

    test = DefProcess.Code('"Пять" if 5 > 4 else "Четыре"')
    Test.Add(service + '.GetArgs', 'normal 2', test, 'Пять')

    test = DefProcess.Code('4 + 2 / 0')
    etalon = '#bug: division by zero'
    Test.Add(service + '.GetArgs', 'unreal', test, etalon)

    test = DefProcess.Code(5 + 7)
    etalon = '#bug: eval() arg 1 must be a string, bytes or code object'
    Test.Add(service + '.GetArgs', 'crash', test, etalon)

    # Run
    test = DefProcess.Run('Tests.Testing', 'Comp', 'fEqual', 9.99, 10)
    Test.Add(service + '.GetArgs', 'normal', test, 0.9, critery=0.99)

    test = DefProcess.Run('Tests.Testing', 'Test', 'Equal', 10, 10)
    Test.Add(service + '.GetArgs', 'crash 1', test, "#bug: type object 'Test' has no attribute 'Equal'")

    test = DefProcess.Run('Tests.Testing', 'Comp', 'Equal', 10, 10, 1)
    Test.Add(service + '.GetArgs', 'crash 2', test, '#bug: Equal() takes 2 positional arguments but 3 were given')

    test = DefProcess.Run('Tests.Testing', 'Comp', 'Equals', 10, 10)
    Test.Add(service + '.GetArgs', 'crash 3', test, "#bug: type object 'Comp' has no attribute 'Equals'")

print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
