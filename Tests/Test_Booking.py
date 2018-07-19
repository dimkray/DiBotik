import certifi
import urllib3
from urllib.parse import urlencode
from urllib.parse import quote

# здесь тестовая обработка #
def Search(stext):
        stext = stext.replace(' ','+')
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        req = format(quote(stext))
        params = {'checkin_month':'3','checkin_monthday':'8','checkin_year':'2018',
                  'checkout_month':'3','checkout_monthday':'9','checkout_year':'2018',
                  'dest_type':'city','group_adults':'1','group_children':'0',
                  'order':'price','raw_dest_type':'city','sb_price_type':'total',
                  'ss':req}
        req = ''
        for param in params:
            req += param +'='+ params[param] +'&'
        print('https://www.booking.com/searchresults.ru.html?'+req)
       
        r = http.request('GET', 'https://www.booking.com/searchresults.ru.html?'+req)
        if r.status == 200:
            d = r.data.decode('ascii','ignore')
            with open('url.html','w') as f:
                f.write(d)
            f.close()
            start = d.find('class="price availprice no_rack_rate')
            if start > 0: # если есть признак цены
                start = d.find('<B>', start + 1)
                end = d.find('</B>', start + 1)
                ftext = d[start+3:end]
                return 'Самая низкая цена: ' + ftext
            else:
                print('#bug: none')
                return '#bug: none'
        else:
            return '#porblem: ' + str(r.status_code)

stest = input('Введите тестовую фразу: ')
print(Search(stest))

import time; time.sleep(5)
