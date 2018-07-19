import Fixer

text = input('Введите тестовую фразу: ')

# здесь тестовая обработка #
t = 0
while text.find('{', t) >= 0:
    t1 = text.find('{', t)
    t2 = text.find('}', t1)
    s = text[t1:t2+1]; ss = ''
    if s.lower() == '{service}': ss = Fixer.Service
    if s.lower() == '{userid}': ss = Fixer.UserID
    if s.lower() == '{chatid}': ss = str(Fixer.ChatID)
    if s.lower() == '{name}': ss = Fixer.Name if Fixer.Name != '' else 'человек'
    if s.lower() == '{family}': ss = Fixer.Family if Fixer.Family != '' else 'без фамилии'
    if s.lower() == '{birthday}': ss = Fixer.BirthDay if Fixer.BirthDay != '' else 'не указан день рождения'
    if s.lower() == '{phone}': ss = Fixer.Phone
    if s.lower() == '{email}': ss = Fixer.eMail
    if ss != '': text = text.replace(s, ss)
    t = t1 + 1

print('Результат тестирования: ' + text)

import time; time.sleep(5)
