# -*- coding: utf-8 -*-
# Сервис работы с сайтами
import Fixer
from Services.URLParser import URL, Parser

# Основной класс работы с сайтами
class Web:
    def Otvet(text):
        #try:
            url = 'https://otvet.mail.ru'
            data = URL.GetData(url + '/search/', text, google=False, bsave=True)
            # поиск текста
            ftext = Parser.Parse(data, sdiv='a', sclass='blue item__text', stype='href')
            stext = Parser.Parse(data, sdiv='a', sclass='blue item__text', stype='text')
            print(ftext)
            print(stext)
            if ftext[0] != '#':
                s = 'Ответ на вопрос: "%s"\n\n' % stext[0]
                data = URL.GetData(url + ftext[0])
                if data[0] != '#':
                    text = Parser.Parse(data, sclass='a--atext-value', stype='text')
                    if text[0] != '#':
                        if len(text[0]) > 500: s += text[0][:500] + '...'
                        else: s += text[0]
                Fixer.htext = url + ftext[0] #назначаем гиперссылку
                return s
            else:
                print('#bug: none')
                return '#bug: none'
##        except Exception as e:
##            Fixer.errlog('Web.Otvet', str(e))
##            return '#bug: ' + str(e) 
