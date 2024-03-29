# -*- coding: utf-8 -*-
# pip install vk_api
# pip install apiai
# pip install geolocation-python
# pip install geopy
# pip install wikipedia
# pip install request
# pip install urllib3
# pip install certifi
# pip install urllib3[secure]
# pip install bs4
# pip install lxml
# pip install feedparser

import config
import Fixer
# import logging
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import PreProcessor
import Processor
import PostProcessor
import Notification

from Chats.Chats import Chat

Author = 2876041
Home = 'ВКонтакте'

login, password = config.DiBotik_log, config.DiBotik_pass
vk = vk_api.VkApi(login, password)

try:
    vk.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
    
longpoll = VkLongPoll(vk)


# Получение информации о пользователе
def getInfo():
    try:
        response = vk.method('users.get',
            {'user_ids': Fixer.UserID,
             'fields': 'about,activities,bdate,books,career,city,connections,contacts,counters,country,domain,education,exports,home_town,interests'})
        if response:
            user = response[0]
            Fixer.Name = user['first_name']
            Fixer.Family = user['last_name']
            if 'about' in user:
                Fixer.About = user['about']
            if 'activities' in user:
                Fixer.Interests.append(user['activities'])
            Fixer.BirthDay = user['bdate']
            if 'books' in user:
                Fixer.Interests.append(user['books'])
            if 'career' in user:
                if 'company' in user['career']:
                    Fixer.Contacts['компания'] = user['career']['company']
                if 'position' in user['career']:
                    Fixer.Contacts['вакансия'] = user['career']['position']
            if 'city' in user:
                Fixer.Contacts['город'] = user['city']['title']
                Processor.coordinates(user['city']['title'])
                Fixer.X = Fixer.Coords[0]
                Fixer.Y = Fixer.Coords[1]
            if 'connections' in user:
                for connect in user['connections']:
                    Fixer.Contacts[connect] = user['connections'][connect]
            if 'contacts' in user:
                if 'mobile_phone' in user['contacts']:
                    Fixer.Phone = user['contacts']['mobile_phone']
                if 'home_phone' in user['contacts']:
                    Fixer.Contacts['телефон'] = user['contacts']['home_phone']
            Fixer.Things.append('Друзья: ' + str(user['counters']['friends']))
            Fixer.Things.append('Группы: ' + str(user['counters']['pages']))
            Fixer.Contacts['страна'] = user['country']['title']
            Fixer.Contacts['VK'] = user['domain']
            if 'interests' in user:
                m = Fixer.getparams(user['interests'], ', ')
                for im in m:
                    Fixer.Interests.append(im)
            return True
    except Exception as e:
        print('Ошибка доступа к информации пользователя '+str(Fixer.UserID)+': '+str(e))
        return False


# Получение контента сообщения по истории сообщений с пользователем (User_id)
def GetMessange(user_id):
    try:
        return vk.method('messages.getHistory',
                         {'user_id': user_id, 'offset': 0, 'count': 1})  # , 'start_message_id': -1
    except:
        return False


# Отправление информации автору
def SendAuthor(text):
    try:
        vk.method('messages.send', {'user_id': int(Author), 'message': text})
        return True
    except:
        return False


# Отправление сообщения пользователю
def SendMessage(text):
    if Fixer.ChatID == 0:
        return False
    text = Fixer.Subs(text)
    if Fixer.bChats == 0:
        vk.method('messages.send', {'user_id': Fixer.UserID, 'message': text})
    elif Fixer.bChats == 2:
        vk.method('messages.send', {'chat_id': Fixer.ChatID, 'message': text})
    else: return False
    Fixer.log('Bot', text)
    if Fixer.UserID != Author:
        SendAuthor('~Уведомление: бот пишет пользователю VK '+str(Fixer.UserID)+': ' + text)
    return True


# сервис локации
def location(scoords):
    #from geolocation.main import GoogleMaps
    from Services.Geo import Geo
    try:
        poz = scoords.find(' ')
        Fixer.Y = float(scoords[:poz])
        Fixer.X = float(scoords[poz:])
        Fixer.LastX.append(Fixer.X)
        Fixer.LastY.append(Fixer.Y)
        mes = 'Твои координаты: ' + str(Fixer.Y) + ', ' + str(Fixer.X) + '\n'
        # Сервис Google.Geocoding
        #my_location = GoogleMaps(api_key=config.GMaps_key).search(lat=Fixer.Y, lng=Fixer.X).first()
        #mes += my_location.formatted_address #+ '\n'
        sAdd = Geo.GetAddress(Fixer.Y, Fixer.X)
        mes += sAdd
        Fixer.Address = sAdd
        Fixer.LastAddress.append(Fixer.Address)
        return mes
    except Exception as e:
        Fixer.errlog('Google.Location', str(e))
        return '#bug: ' + str(e)


# Основной вызов API VK
def LongPoll():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            Fixer.bChats = 0
            if event.from_user:
                if event.user_id != Author:
                    SendAuthor('~Уведомление: пользователь VK %i пишет: %s' % (event.user_id, event.text))
            elif event.from_chat:
                Fixer.bChats = 1  # признак чата
                if event.text.upper()[:3] == 'DI,' or event.text.upper()[:3] == 'ДИ,': Fixer.bChats = 2 # надо ответить
                if event.user_id != Author:
                    SendAuthor('~Уведомление: пользователь VK %i пишет в беседе %i: %s' % (event.user_id, event.chat_id, event.text))
            elif event.from_group:
                Fixer.bChats = 1  # признак чата
                if event.user_id != Author:
                    SendAuthor('~Уведомление: пользователь VK %i пишет в группе %i: %s' % (event.user_id, event.group_id, event.text))

            if Fixer.bChats == 1:
                continue  # пропускаем беседу
            # Обработка сообщений для бота
            if event.to_me:
                text = event.text
                try:
                    if len(text) > 3:
                        if text.upper()[:3] == 'DI,' or text.upper()[:3] == 'ДИ,': text = text[3:].strip()
                    Fixer.ChatID = event.chat_id
                    Fixer.PeerID = event.peer_id
                    # Идентификатор юзера
                    Fixer.UserID = event.user_id
                    Msg = GetMessange(Fixer.UserID)['items'][0]
                    print(Msg)  # печать сообщения
                    Fixer.Time.append(Fixer.time())
                    Fixer.Chat.append(text)
                    if Chat.Load() == False:
                        # Получение информации о пользователе
                        getInfo()
                        print('Данные не найдены')
                    Fixer.Mess = Home
                    # Бот начинает писать текст
                    vk.method('messages.setActivity', {'user_id': Fixer.UserID, 'chat_id': Fixer.ChatID, 'type': 'typing'})
                    # Поиск текущей локации пользователя
                    if 'geo' in Msg:
                        Fixer.Process = 'Bot.GetUserLocation'
                        geo = Msg['geo']
                        s = ''
                        if 'coordinates' in geo:
                            s = location(geo['coordinates']) + '\n'
                        if 'place' in geo:
                            if 'country' in geo['place']:
                                s += geo['place']['country'] + ', '
                            if 'city' in geo['place']:
                                s += geo['place']['city']
                        if text == '':
                            SendMessage(s)
                            Chat.Save()
                            continue
                    # Поиск стикеров и вложений
                    if 'attachments' in Msg:
                        iphoto = 0
                        Fixer.Process = 'Bot.GetUserAttachments'
                        for att in Msg['attachments']:  # иттератор по вложениям
                            if att['type'] == 'sticker':  # найден стикер
                                SendMessage('Сорян. Я не умею распознавать стикеры.'); continue
                            elif att['type'] == 'photo':  # найдено фото
                                iphoto += 1
                            else: # другой тип вложения
                                if text == '':
                                    SendMessage('В данных типах вложениях я не разбираюсь :('); continue
                        if iphoto > 0:
                            if iphoto == 1:
                                s = 'Одно фото во вложении. В будующем смогу провести анализ фото :)'
                            elif iphoto > 1:
                                s = 'Найдено '+str(iphoto) + ' изображений/фото во вложении.'
                            SendMessage(s)
                            continue  # пропускаем сообщение
                    # ------------ основная обработка пользовательских сообщений ---------------
                    else:
                        # Мультипроцессорный обработчик - когда в одном сообщении сразу несколько запросов
                        mProcess = PreProcessor.MultiProcessor(text)
                        print(mProcess)
                        for itext in mProcess:
                            # Препроцессорный обработчик
                            Fixer.Process = 'Bot.PreProcessor'
                            request = PreProcessor.ReadMessage(itext)
                            # Процессорный обработчик
                            Fixer.Process = 'Bot.Processor'
                            request = Processor.FormMessage(request)
                            Fixer.log('Processor', request)
                            if request[0] == '#':  # Требуется постпроцессорная обработка
                                request = PostProcessor.ErrorProcessor(request)
                                if request[:6] == '#LOC! ':  # Требуется определить геолокацию
                                    # !Доработать блок!
                                    request = location(str(Fixer.Y) + ' ' + str(Fixer.X))
                                    request += '\nДля определения более точных координаты в VK, прикрепи и отправь мне текущее местоположение на карте.'
                                Fixer.log('PostProcessor', request)
                                SendMessage(request)
                            else: # Постпроцессорная обработка не требуется
                                if Fixer.Service != '':
                                    Fixer.LastService.append(Fixer.Service)
                                SendMessage(request)
                            if Fixer.htext != '':  # если есть гипперссылка/ки
                                Fixer.log('HiperText', Fixer.htext)
                                slink = 'Ссылка: '  # если одна ссылка
                                if '\n' in Fixer.htext:
                                    slink = 'Ссылки:'
                                    Fixer.htext = slink + Fixer.htext
                                else:
                                    Fixer.htext = slink + Fixer.htext.replace(' ', '%20')
                                SendMessage(Fixer.htext)
                                Fixer.htext = ''
                        Chat.Save()
                    Notification.Process()  # запуск системы уведомлений
                except Exception as e:
                    s = str(e)
                    Fixer.errlog(Fixer.Process, str(e))
                    SendMessage(PostProcessor.ErrorProcessor('#critical: ' + s))


# Основной блок программы
if __name__ == '__main__':
    # Настройка логгирования
    # log = logging.getLogger('Bot')
    # log.setLevel(logging.INFO)
    # fh = logging.FileHandler("DiBot.log")
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # log.addHandler(fh)

    Fixer.log('Start', '--------------------------------------------')
    Fixer.log('Start', 'Запуск VK-Бота')
    Fixer.log('Start', '--------------------------------------------')
    SendAuthor('Рестарт DiBot!')

    # Запуск LongPoll
    LongPoll()
