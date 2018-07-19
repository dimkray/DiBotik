from Profiler import Profiler
from Tests.Testing import Test, Report
from Services.Service_ import Service_

service = 'Service_'

print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #
with Profiler() as p:
    # isWork
    test = Service_.Go('тест')
    Test.Add(service+'.Function','тестирование функции', test, 0)

print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
