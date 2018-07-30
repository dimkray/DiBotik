# -*- coding: utf-8 -*-
# Сервис автотестирования бота
import Fixer

# Измерение расстояние от одной точки до другой
def Alltests():
    try:
        import Tests.Test_Yandex

    except Exception as e:
        Fixer.errlog('SMath.Distance', str(e))
        return '#bug: ' + str(e) 
