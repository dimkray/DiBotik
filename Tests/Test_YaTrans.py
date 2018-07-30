from Services.Yandex import Ya

bwork = True
while bwork:
    stest = input('Введите тестовую фразу: ')

    # здесь тестовая обработка #
    stest = Ya.Translate(stest, 'авто', 'английский')

    print('Результат тестирования: ' + stest)

    if stest == 'выход' or stest == 'exit':
        bwork = False
