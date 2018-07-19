import requests

# поиск локации
r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
if r.status_code != requests.codes.ok:
    print('Ошибка подключения к сервису: ' + r.status_code)
data = r.json()
vals = data['Valute']

b = True
while b:
    try:
        val = input('Введите тестовый запрос: ').upper()
        print(val + ': ' + str(vals[val]['Value']) +' руб за ' + str(vals[val]['Nominal']) + ' ' + val)
    except Exception as e:
        #Fixer.errlog('Ошибка в сервисе Google.Shorten!: ' + str(e))
        print('#bug: ' + str(e))

import time; time.sleep(5)
