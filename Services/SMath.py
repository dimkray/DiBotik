# -*- coding: utf-8 -*-
# Простой сервис математики
import math
import Fixer

# Измерение расстояние от одной точки до другой
def Distance(x1,y1,x2,y2):
    try:
        return math.sqrt((x1 - x2)**2+(y1 - y2)**2)
    except Exception as e:
        Fixer.errlog('SMath.Distance', str(e))
        return '#bug: ' + str(e) 
