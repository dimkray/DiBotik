from Services.Yandex import Yandex

bwork = True
while bwork:
    stest = input('Введите тестовую фразу: ')

    # здесь тестовая обработка #
    stest = Yandex.Speller(stest)

    print('Результат тестирования: ' + stest)

    if stest == 'выход' or stest == 'exit':
        bwork = False
