# -*- coding: utf-8 -*-
# Сервис ОГРН.Онлайн - информация о ЮЛ и ИП
import Fixer
import config
from Services.URLParser import URL
from urllib.parse import quote

url = 'https://xn--c1aubj.xn--80asehdb'
test = format(quote('/интеграция/компании/'))
ogrn_header = {'X-ACCESS-KEY': config.ogrn_key}

# Получение основной информации
class info:
    def test():
        try:
            print(URL.GetData(url+test, 'СТРОЙПРОЕКТ', 'наименование', params={'стр':2}, headers=ogrn_header))
        except Exception as e:
            Fixer.errlog('ogrn.Name', str(e))
            return '#bug: ' + str(e) 

# тест
info.test()
