import Fixer
import requests

# Класс курсы валют. Для работы вначале нужно вызвать GetRates
class Rate:
    Vals = {} # все валюты

    # Проверка наличия валюты
    def isValute(valute):
        if valute in Rate.Vals: return True
        return False
    
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
            if Rate.isValute(valute) == False: return('#problem: ' + valute)
            rez = Rate.Vals[valute]['Value'] / Rate.Vals[valute]['Nominal']
            return(str(round(rez, 2)))
        except Exception as e:
            Fixer.errlog('Rates.RateRub', str(e))
            return('#bug: ' + str(e))

    # Получение курса валюты из расчёта на 1 рубль
    # На входе идентификатор валюты в формате: USD, EUR и т.д.
    def RateFromRub(valute):
        try:
            if len(Rate.Vals) == 0: Rate.GetRates()
            if valute == 'RUB': return 1
            if Rate.isValute(valute) == False: return('#problem: ' + valute)
            rez = Rate.Vals[valute]['Nominal'] / Rate.Vals[valute]['Value']
            return(str(round(rez, 2)))
        except Exception as e:
            Fixer.errlog('Rates.RateFromRub', str(e))
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
                if Rate.isValute(valute1) == False: return('#problem: ' + valute1)
                rubs = value * Rate.Vals[valute1]['Value'] / Rate.Vals[valute1]['Nominal']
            # конвертация во вторую валюту
            if valute2 == 'RUB':
                return str(round(rubs, 2))
            else:
                if Rate.isValute(valute2) == False: return('#problem: ' + valute2)
                rez = rubs * Rate.Vals[valute2]['Nominal'] / Rate.Vals[valute2]['Value']
                return str(round(rez, 2))
        except Exception as e:
            Fixer.errlog('Rates.RateRub', str(e))
            return('#bug: ' + str(e))
        
