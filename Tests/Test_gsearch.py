from Services.Google import Google
from Services.Geo import Geo
import Fixer

x = float(input('Введите координату X: '))
y = float(input('Введите координату Y: '))

# здесь тестовая обработка #
stest = Geo.GetAddress(x,y)

print('Результат тестирования: ' + stest)

import time; time.sleep(5)
