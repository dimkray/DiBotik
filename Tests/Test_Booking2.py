from Services.URLParser import URL, Parser

# здесь тестовая обработка #
def Search(stext):
        params = {'checkin_month':'4','checkin_monthday':'8','checkin_year':'2018',
                  'checkout_month':'4','checkout_monthday':'9','checkout_year':'2018',
                  'dest_type':'city','group_adults':'1','group_children':'0',
                  'order':'price','raw_dest_type':'city','sb_price_type':'total'}
        data = URL.GetData('https://www.booking.com/searchresults.ru.html',
                           stext=stext, textparam='ss', params=params, brequest=False, bsave=True)
        if data[0] != '#':
            d = Parser.Find(data, 'class="price availprice no_rack_rate', '<B>', '</B>')
            print(d)
            return True
        else:
            return False

stest = input('Введите тестовую фразу: ')
print(Search(stest))

import time; time.sleep(5)
