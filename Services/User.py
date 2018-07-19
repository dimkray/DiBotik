# -*- coding: utf-8 -*-
# Сервис обработки сообщений о пользователе
import Fixer
import Bot

def getpar(text, separator=','):
    print(text.split(separator))
    return text.split(separator)

class User:
    # ообработка основной информации о пользователе
    def Info(param, text):
        try:
            if param == 'age': # возраст
                try:
                    Fixer.Age = int(text)
                    s = str(Fixer.Age) +Fixer.Dialog('age_get')
                    if Fixer.Age < 10: s = 'Какой-то ты совсем маленький!'
                    if Fixer.Age > 100: s = 'Ух, ты! Да ты видел Ленина!'
                    Bot.SendMessage(s)
                except:
                    return 'Хм... Не понял... Напиши лучше свой возраст цифрами.'
            if param == 'name': # Имя
                Fixer.Name = text
                Bot.SendMessage('Тебя зовут ' + Fixer.Name +'! Хорошо! Запомнил :)')
            if param == 'type': # Тип
                s = text[6:8]
                if s.lower() == 'да' or s.lower() == 'аг' or s.lower() == 'му':
                    Fixer.Type = 1
                    s = 'мужчина'
                else:
                    Fixer.Type = 2
                    s = 'женщина'
                Bot.SendMessage('Хорошо! Понял, что '+s+' :)')
            if param == 'birthday': # День Рождения
                Fixer.BirthDay = text
                Bot.SendMessage('Хорошо! Запомнил и непременно поздравлю в этот день! :)')
            if param == 'family': # Фамилия
                Fixer.Family = text
                Bot.SendMessage(Fixer.Name +' '+ Fixer.Family +'! Хорошо! Запомнил :)')
            if param == 'phone': # Телефон
                Fixer.Phone = text
                Bot.SendMessage('Хорошо! Запомнил :)')
            if param == 'email': # eMail
                Fixer.eMail = text
                Bot.SendMessage('Хорошо! Запомнил :)')
            if param == 'interest': # Интересы
                m = getpar(text)
                for i in m:
                    i = i.strip().lower()
                    Fixer.Interests.append(i)
                Bot.SendMessage('Хорошо! Запомнил интересы :)')
            if param == 'contact': # контакты
                m = text.split(' | ')
                if len(m) == 1:
                    Fixer.Contacts['vk'] = m[0]
                else:
                    Fixer.Contacts[m[0]] = m[1]
                Bot.SendMessage('Хорошо! Запомнил контакт :)')	
            if param == 'thing': # вещи/собсвенность
                i = text.strip().lower()
                Fixer.Interests.append(i)
                Bot.SendMessage('Хорошо! Я это запомнил :)')				
            return User.Acquaintance()
        except Exception as e:
            Fixer.errlog('User.Info', str(e))
            return '#bug: ' + str(e)

    # сервис знакомства
    def Acquaintance():
        from DB.SQLite import SQL
        Fixer.bAI = False
        Fixer.Context = True
        if Fixer.Name == '' or Fixer.Name == 'человек':
            Fixer.Service = 'user-name'
            return Fixer.Dialog('bot_about')
        if Fixer.Type == 0:
            rName = SQL.ReadRow('names', 'nameU', Fixer.Name.upper().replace('Ё','Е'))
            if len(rName) > 0:
                if rName[1] == 1: # мужчина
                    Fixer.Type = 1
                else:
                    Fixer.Type = 2
            if Fixer.Type == 0: # если не удалось определить пол по имени
                Fixer.Service = 'user-type'
                return 'Извини за нескромный вопрос. Ты мужчина?'
        if Fixer.Age == 0:
            Fixer.Service = 'user-age'
            return 'А сколько тебе лет?'
        if Fixer.BirthDay == '' or Fixer.BirthDay == 'день рождения не известен':
            Fixer.Service = 'user-birthday'
            return 'Я родился совсем недавно. Меня начали создавать буквально пару месяцев назад - в феврале 2018 года.\nА какого числа родился ты?'
        if Fixer.Family == '' or Fixer.Family == 'без фамилии':
            Fixer.Service = 'user-family'
            return 'Напиши свою фамилию. Это на всякий случай'
        if Fixer.Phone == '' or Fixer.Phone == 'телефон не указан':
            Fixer.Service = 'user-phone'
            return 'Напиши, пожалуйста, свой телефон для связи'
        if Fixer.eMail == '' or Fixer.eMail == 'e-mail не указан':
            Fixer.Service = 'user-email'
            return 'Напиши, пожалуйста, свой e-mail для связи'
        if len(Fixer.Contacts) == 0:
            Fixer.Service = 'user-contact'
            return 'Напиши адрес странички в контакте, если он у тебя есть'
        if len(Fixer.Interests) == 0:
            Fixer.Service = 'user-interest'
            return 'Я создан для агрегации всех полезных сервисов для путешественников.\nА чем ты увлекаешься?\nПеречисли через запятую свои интересы'
        Fixer.Service = ''; Fixer.Thema = ''
        Fixer.bAI = True; Fixer.Context = False
        return 'Чем я тебе могу помочь?'
