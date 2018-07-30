import Fixer
from Services.Yandex import Ya

stest = input('Введите тестовую фразу: ')

# здесь тестовая обработка #
stest = Ya.Catalog(stest)

print('Результат тестирования: ' + stest)

import time; time.sleep(5)
