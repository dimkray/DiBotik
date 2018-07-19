# -*- coding: utf-8 -*-
# Сервис по работе с подбором жилья (отели, хостелы, квартиры)
import Fixer
#from Services.URLParser import URL, Parser
from Services.House import Booking

# Тест
text = input('Введите город: ')
mlist = Booking.List(text,'2018-05-10','2018-05-11', people=1, order='price', dorm=True)
for item in mlist:
    print(item)
print(Fixer.htext)
