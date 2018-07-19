import Fixer
from Services.Yandex import Yandex

stest = input('Введите тестовую фразу: ')

# здесь тестовая обработка #
stest = Yandex.Catalog(stest)

print('Результат тестирования: ' + stest)

import time; time.sleep(5)
