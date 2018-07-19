import Fixer
import pickle

class Chat:
    # Функция записи данных о текущем пользователе (по id chat)
    def Save():
        try:
            data = { 'version': 20180427,
                     'chat': [Fixer.Time, Fixer.Chat, Fixer.Response],
                     'user': [Fixer.UserID, Fixer.Name, Fixer.Family, Fixer.BirthDay, Fixer.Age,
                     Fixer.Type, Fixer.Thema, Fixer.LastThema, Fixer.Service, Fixer.LastService,
                     Fixer.Phone, Fixer.eMail, Fixer.Contacts, Fixer.Interests, Fixer.Things, 
                     Fixer.bNotice, Fixer.TimeZone],
                     'location': [Fixer.X, Fixer.Y, Fixer.LastX, Fixer.LastY, 
                                  Fixer.Address, Fixer.LastAddress,
                                  Fixer.Coords, Fixer.LastCoords],
                     'translate': [Fixer.Lang1, Fixer.Lang2, Fixer.Ttext.replace('\n',' '),
                     Fixer.LastLang1, Fixer.LastLang2],
                     'rasp': [Fixer.nameSt, Fixer.region, Fixer.iTr, Fixer.St1, Fixer.St2, 
                     Fixer.trDate, Fixer.LastSt1, Fixer.LastSt2, Fixer.LastTr],
                     'wiki': [Fixer.Page, Fixer.LastPage, Fixer.WikiStart],
                     'rate': [Fixer.Valute, Fixer.LastValute],
                     'notes': Fixer.Notes,
                     'rss': [Fixer.RSS, Fixer.LastRSS]}
            f = open('Chats\\' + str(Fixer.ChatID) + '.chat', 'wb')
            pickle.dump(data, f)
            f.close()
            return data # возвращает текущее состояние для #Fixer
        except Exception as e:
            Fixer.errlog(Fixer.Process, str(e))
            return '#bug: ' + str(e)

    # Функция загрузки данных о текущем пользователе (по id chat)
    def Load():
        try:
            if Fixer.Exists('Chats\\' + str(Fixer.ChatID) + '.chat') == False: return False
            f = open('Chats\\' + str(Fixer.ChatID) + '.chat', 'rb')
            data = pickle.load(f)
            Fixer.Version = data['version']
            d = data['chat']
            Fixer.Time = d[0]
            Fixer.Chat = d[1]
            if Fixer.Version >= 20180320: Fixer.Response = d[2]
            
            d = data['user']
            Fixer.UserID = d[0]
            Fixer.Name = d[1]
            Fixer.Family = d[2]
            Fixer.BirthDay = d[3]
            Fixer.Age = d[4]
            Fixer.Type = d[5]
            Fixer.Thema = d[6]
            Fixer.LastThema = d[7]
            Fixer.Service = d[8]
            Fixer.LastService = d[9]
            if Fixer.Version >= 20180320:
                Fixer.Phone = d[10]
                Fixer.eMail = d[11]
                Fixer.Contacts = d[12]
                Fixer.Interests = d[13]
            if Fixer.Version >= 20180322: Fixer.Things = d[14]
            if Fixer.Version >= 20180323: Fixer.bNotice = d[15]
            if Fixer.Version >= 20180405: Fixer.TimeZone = d[16]
			
            d = data['location']
            Fixer.X = d[0]
            Fixer.Y = d[1]
            Fixer.LastX = d[2]
            Fixer.LastY = d[3]
            Fixer.Address = d[4]
            Fixer.LastAddress = d[5]
            if Fixer.Version >= 20180320:
                Fixer.Coords = d[6]
                Fixer.LastCoords = d[7]
            
            d = data['translate']
            Fixer.Lang1 = d[0]
            Fixer.Lang2 = d[1]
            Fixer.Ttext = d[2]
            Fixer.LastLang1 = d[3]
            Fixer.LastLang2 = d[4]
            
            d = data['rasp']
            Fixer.nameSt = d[0]
            Fixer.region = d[1]
            Fixer.iTr = d[2]
            Fixer.St1 = d[3]
            Fixer.St2 = d[4]
            Fixer.trDate = d[5]
            Fixer.LastSt1 = d[6]
            Fixer.LastSt2 = d[7]
            Fixer.LastTr = [8]
            
            d = data['wiki']
            Fixer.Page = d[0]
            Fixer.LastPage = d[1]
            if Fixer.Version >= 20180328: Fixer.WikiStart = d[2]
            
            d = data['rate']
            Fixer.Valute = d[0]
            Fixer.LastValute = d[1]
            
            if Fixer.Version >= 20180320:
                Fixer.Notes = data['notes']
            
            if Fixer.Version >= 20180427:
                d = data['rss']
                Fixer.RSS = d[0]
                Fixer.LastRSS = d[1]

            f.close()
            return True
        except Exception as e:
            Fixer.errlog(Fixer.Process, str(e))
            return False
