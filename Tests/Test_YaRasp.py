from Services.Yandex import Yandex

# Обработка результатов сервиса Яндекс.Расписание
def FormRasp(s):
    global htext
    tstr = s
    if s[0] == '%': # Рейсы найдены!
        nstr = s.find(' ',1)
        num = int(s[1:nstr]) # количество рейсов
        gstr = s.find('#',1)
        htext = s[gstr+1:]
        routes = s[nstr+1:gstr-2].strip().split('\n')
        if num == 0:
            tstr = 'Печалька. Не нашёл ни одного рейса :(\nМожет я не правильно тебя понял? Попробуй по другому сделать запрос!'
        elif 0 < num < 11:
            tstr = 'Нашёл ' + str(num) + ' рейс(ов)!\n'
        elif 10 < num < 300:
            tstr = 'Нашёл ' + str(num) + ' рейс(ов). Покажу первые 10.\n'
        elif 300 < num < 1000:
            tstr = 'Нашёл дохрена рейсов! ' + str(num) + '! Покажу первые 10.\n'
            tstr += s[num+1:gstr]
        else:
            tstr = 'Нашёл какое-то невероятное число рейсов! ' + str(num) + '! Может я где-то ошибся? Лучше зайди по ссылке, посмотри всё ли правильно.\n'
        if num > 0:
            x = 0
            for rout in routes:
                tstr += routes[x] + '\n'
                x += 1
                if x > 11: break
        if len(routes)-1 != num: # части рейсов нет
            tstr += '\n' + str(num-len(routes)-1) + 'рейс\рейсов на сегодня уже нет.'
        if len(routes)-1 == 0 and num > 0: # если уже рейсов нет
            tstr = 'На сегодня уже нет ни одного рейса :('
    return tstr

global htext
bwork = True
while bwork:
    stest = input('Введите тестовую фразу: ')
    
    # здесь тестовая обработка #
    tstr = ''; gstr = ''
    tsend = Yandex.FindRasp(stest)
    tsend = FormRasp(tsend)
    print(tsend)

    
    print('Результат тестирования:\n' + tsend)
    #print(htext)

    if tsend == 'выход' or tsend == 'exit':
        bwork = False
