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
                    price = Parser.Parse(item, sdiv='strong', sclass='price availprice no_rack_rate ', stype='text')
                    sRt = ''
                    if score[0][0] == '#': score[0] = ''; sRt ='нет оценки'
                    if price[0][0] == '#': price[0] = 'не указана'
                    if score[0] != '':
                        score[0] = score[0].replace(',','.')
                        if float(score[0]) <= 3: sRt = 'хрень полная!'
                        elif 3 < float(score[0]) <= 5: sRt = 'отстой'
                        elif 5 < float(score[0]) <= 6: sRt = 'так себе'
                        elif 6 < float(score[0]) <= 7: sRt = 'жить можно'
                        elif 7 < float(score[0]) <= 8: sRt = 'хорошо'
                        elif 8 < float(score[0]) <= 9: sRt = 'великолепно'
                        elif 9 < float(score[0]) <= 9.5: sRt = 'потрясающе'
                        elif 9.5 < float(score[0]) < 10: sRt = 'превосходно'
                        elif 9 < float(score[0]) == 10: sRt = 'охренительно!'
                        else: sRt = 'этой оценке не придумали названия'
                    mList.append('Название: %s\nОценка: %s (%s). Стоимость от: %s' % (name[0], score[0], sRt, price[0]))
            return mList
        except Exception as e:
            Fixer.errlog('House.Booking', str(e))
            return '#bug: ' + str(e) 
