import DefProcess
from Profiler import Profiler
from Tests.Testing import Test, Report
from Services import _Service_
from Services._Service_ import _Serv_


service = '_Service_'
print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #

# _Def_
sdef = '._Def_'
with Profiler() as p:
    test = _Service_._Def_('Русский')
    etalon = 'ru'
Test.Add(service, service + sdef, 'normal', test, etalon)

with Profiler() as p:
    test = _Service_._Def_('Элийский')
    etalon = ''
Test.Add(service, service + sdef, 'unreal', test, etalon)


service = '_Serv_'
# Добавляем все функции класса
for idef in DefProcess.GetMemberList(_Serv_):
    Test.AddDef(service, service + '.' + idef)

sdef = '._Def_'
with Profiler() as p:
    test = _Serv_._Def_('taxcom')
    etalon = ""
Test.Add(service, service + sdef, 'normal', test, etalon)

with Profiler() as p:
    test = _Serv_._Def_('xxxx')
    etalon = ""
Test.Add(service, service + sdef, 'unreal', test, etalon)

with Profiler() as p:
    test = _Serv_._Def_(0)
    etalon = "#bug: ..."
Test.Add(service, service + sdef, 'crush', test, etalon)


print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())

print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
