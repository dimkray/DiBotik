# -*- coding: utf-8 -*-
import random

# создаём словарь
d = {'x':['1','2','3','4'],
     'y':['1','2','3','4']}

x = 0
while x < 10:
    print(random.choice(d['x']))
    print(random.choice(d['y']))
    x += 1
