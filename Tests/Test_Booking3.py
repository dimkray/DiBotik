# -*- coding: utf-8 -*-
# Сервис по работе с подбором жилья (отели, хостелы, квартиры)
import Fixer
from Services.URLParser import URL, Parser

class Booking: # Работа с booking.com
    # 'score' - по оценке
    # 'center' - поближе к центру
    # 'optimal' - цена/качество
    # people=2.3 - два взрослых и 3 ребёнка
    # dorm - допустимость совместного проживания с кем-то
    # checkin, checkout = формат: YYYY-MM-DD
    def List(city, checkin, checkout, people=1.0, order='price', dorm=True):
        try:
            mList = []
            mdate1 = checkin.split('-')
            mdate2 = checkout.split('-')
            if order == 'optimal': order = 'review_score_and_price'
            if order == 'center': order = 'distance_from_landmark'
            adult = int(people)
            child = int(10*(people-int(people)))
            params = {'checkin_month':mdate1[1],'checkin_monthday':mdate1[2],'checkin_year':mdate1[0],
                  'checkout_month':mdate2[1],'checkout_monthday':mdate2[2],'checkout_year':mdate2[0],
                  'dest_type':'city','group_adults':adult,'group_children':child,
                  'order':order,'raw_dest_type':'city','sb_price_type':'total'}
            if dorm == False: params['no_dorms'] = '1'
            if order == 'distance_from_landmark' : params['dst_landmark'] = 'cc'
            url = URL.GetURL('https://www.booking.com/searchresults.ru.html', stext=city, textparam='ss', params=params)
            Fixer.htext = url
            texturl = URL.OpenURL(url)
            if texturl[0] != '#':
                mItems = Parser.Parse(texturl, sclass='sr_item_content sr_item_content_slider_wrapper ', stype='all')
                for item in mItems:
                    name = Parser.Parse(item, sdiv='span', sclass='sr-hotel__name', stype='text')
                    score = Parser.Parse(item, sdiv='span', sclass='review-score-badge', stype='text')
                    print(score)
                    price = Parser.Parse(item, sdiv='strong', sclass='price availprice no_rack_rate ', stype='text')
                    print(price)
                    if score[0][0] == '#': score[0] == 'нет оценки'
                    if price[0][0] == '#': price[0] == 'не указана'
                    mList.append('Название: %s\nОценка: %s Стоимость от: %s' % (name[0], score[0], price[0]))
            return mList
        except Exception as e:
            Fixer.errlog('Booking.List', str(e))
            return '#bug: ' + str(e) 

# Тест
text = input('Введите город: ')
mlist = Booking.List(text,'2018-04-10','2018-04-11', people=1, order='optimal', dorm=False)
for item in mlist:
    print(item)
print(Fixer.htext)
