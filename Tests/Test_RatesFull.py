import Fixer
import requests

# Класс курсы валют. Для работы вначале нужно вызвать GetRates
class Rate:
    Vals = {} # все валюты

    # Запрос на курсы валют    
    def GetRates():
        # Сервис ЦБ РФ по курсам валют 
        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        if r.status_code != requests.codes.ok:
            return('#problem: ' + r.status_code)
        data = r.json()
        Rate.Vals = data['Valute']

    # Получение курса валюты в рублях
    # На входе идентификатор валюты в формате: USD, EUR и т.д.
    def RateRub(valute):
        try:
            if len(Rate.Vals) == 0: Rate.GetRates()
            if valute == 'RUB': return 1
            return(Rate.Vals[valute]['Value'] / Rate.Vals[valute]['Nominal'])
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Rates.RateRub!: ' + str(e))
            return('#bug: ' + str(e))

    # Получение курса валюты из расчёта на 1 рубль
    # На входе идентификатор валюты в формате: USD, EUR и т.д.
    def RateFromRub(valute):
        try:
            if len(Rate.Vals) == 0: Rate.GetRates()
            if valute == 'RUB': return 1
            return(Rate.Vals[valute]['Nominal'] / Rate.Vals[valute]['Value'])
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Rates.RateFromRub!: ' + str(e))
            return('#bug: ' + str(e))
        
    # Конвертация одной валюты в другую
    # На входе идентификатор валюты в формате: USD, EUR и т.д.
    def RateRubValue(valute1, valute2, value=1):
        try:
            if len(Rate.Vals) == 0: Rate.GetRates()
            # перевод в рубли
            if valute1 == 'RUB':
                rubs = value
            else:
                rubs = value * Rate.Vals[valute1]['Value'] / Rate.Vals[valute1]['Nominal']
            # конвертация во вторую валюту
            if valute2 == 'RUB':
                return rubs
            else:
                return rubs * Rate.Vals[valute2]['Nominal'] / Rate.Vals[valute2]['Value']
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Rates.RateRub!: ' + str(e))
            return('#bug: ' + str(e))

# тестовая часть программы
rate1 = Rate.RateRub(input('валюта: '))
print(rate1)
rate2 = Rate.RateFromRub(input('валюта: '))
print(rate2)
val1 = input('валюта1: ')
val2 = input('валюта2: ')
val = float(input('значение: '))
rate3 = Rate.RateRubValue(val1,val2,val)
print(rate3)
