# -*- coding: utf-8 -*-
# Сервис уведомлений
import Bot
import Fixer
import Processor
from Chats.Chats import Chat
from datetime import datetime, timedelta

# -------------------------------
# Все задания на уведомления
# -------------------------------
# Структура хранения данных
# key - название уведомления "UserID:Type-Number" : [
# 0 - вкл/выкл уведомление (bool),
# 1 - время срабатывания задачи (time),
# 2 - дельта для следующего повторения (time),
# 3 - число повторений (int), 0 - повторять бесконечно (до отключения задания)
# 4 - сообщение для пользователя (str),
# 5 - запускаемый сервис (str) ]
Tasks = {}

#-----------------------------------
# Сервис уведомлений (по сервису #task)
#-----------------------------------
def Process():
    try:
        bChange = False; delKeys = []
        Tasks = Fixer.LoadB('Tasks')
        #if Tasks != {}: print(Tasks)
        if len(Tasks) == 0: return False # print('Ошибка загрузки или пустой Tasks.db!');
        tdate = datetime.today()
        for t in Tasks:
            if Tasks[t][0] == False: continue # уведомление отключено
            if Tasks[t][1] < tdate: # время для запуска задачи!
                print(t[:t.find(':')])
                Fixer.ChatID = t[:t.find(':')]
                Chat.Load() # загрузка данных пользователя
                bChange = True
                request = Tasks[t][4]
                if Tasks[t][5] != '':
                    # Процессорный обработчик
                    request = Processor.FormMessage(Tasks[t][5])
                    Fixer.log('Processor', request)
                if request != '': 
                    Fixer.log('Notification',str(Tasks[t][1]) + ' Запуск задачи "'+t+'"!')
                    Bot.SendMessage(request)
                Tasks[t][1] += Tasks[t][2] # установка времени на следующий цикл
                if Tasks[t][3] > 1: # Уменьшаем цикл
                    Tasks[t][3] -= 1
                elif Tasks[t][3] == 1: # Удаляем задание
                    delKeys.append(t)
        if len(delKeys) > 0: # отложенное удаление задач
            for k in delKeys:
                del(Tasks[k])
        if bChange:
            print(Tasks)
            Fixer.SaveB(Tasks, 'Tasks')
    except Exception as e:
        Fixer.errlog('Notification', str(e))                              
