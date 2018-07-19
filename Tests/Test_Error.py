import Fixer

stest = input('Введите тестовую фразу: ')

# здесь тестовая обработка #
try:
    test = '10'+10
except Exception as e:
    Fixer.errlog('Test', 'Ошибка в тесте!: ' + str(e))
    print('#bug: ' + str(e))

import time; time.sleep(5)
