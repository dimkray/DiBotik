from Profiler import Profiler
from Tests.Testing import Test, Report
from Services.StrMorph import String, Word, Modif

service = 'StrMorth'

print('------- Запущены тесты сервиса %s --------' % service)

# здесь тестовая обработка #
with Profiler() as p:
    # StringsCount
    test = String.StringsCount('Предложение один. Предложение два! Предложение три?!!! Четыре... !')
    Test.Add(service+'.StringsCount','normal', test, 5)

    test = String.StringsCount(' ')
    Test.Add(service+'.StringsCount','unreal', test, 0)

    test = String.StringsCount(5)
    Test.Add(service+'.StringsCount','crash', test, 0)

    # GetStrings
    test = String.GetStrings('Предложение один. Предложение два! Предложение три?!!! Четыре... !')
    etalon = ['Предложение один.','Предложение два!','Предложение три?!!!','Четыре...','!']
    Test.Add(service+'.GetStrings','normal 1', test, etalon)

    test = String.GetStrings('1\n2\n\nполянка!на ! теле')
    etalon = ['1','2','полянка!на !','теле']
    Test.Add(service+'.GetStrings','normal 2', test, etalon)

    test = String.GetStrings(' ')
    Test.Add(service+'.GetStrings','unreal', test, [])

    test = String.GetStrings({'Слово':67})
    Test.Add(service+'.GetStrings','crash', test, [])

    # WordsCount
    test = String.WordsCount('Предложение - один. Пре-дложение два! Предложение три?!!! Четыре... 5 + !')
    Test.Add(service+'.WordsCount','normal', test, 9)

    test = String.WordsCount(' ')
    Test.Add(service+'.WordsCount','unreal', test, 0)

    test = String.WordsCount(5)
    Test.Add(service+'.WordsCount','crash', test, 0)    

    # GetWords
    test = String.GetWords('Предложение - один. Пре-дложение два! Предложение три?!!! Четыре... 5 + !')
    etalon = ['Предложение','один','Пре','дложение','два','Предложение','три','Четыре','5']
    Test.Add(service+'.GetWords','normal', test, etalon)

    test = String.GetWords(' ')
    Test.Add(service+'.GetWords','unreal', test, [])

    test = String.GetWords(5)
    Test.Add(service+'.GetWords','crash', test, [])

    # GetConstr
    test = String.GetConstr('Сервис по - проверке и оплате штрафов ГИБДД; через интернет онлайн. Вы + !')
    etalon = '[Сервис] [по] - [проверке] [и] [оплате] [штрафов] [ГИБДД]; [через] [интернет] [онлайн]. [Вы] + !'
    Test.Add(service+'.GetConstr','normal', test, etalon)

    test = String.GetConstr(' ')
    Test.Add(service+'.GetConstr','unreal', test, ' ')

    test = String.GetConstr(5)
    Test.Add(service+'.GetConstr','crash', test, 5)

    # Tags
    test = Word.Tags('Табареками')
    Test.Add(service+'.Tags','normal 1', test, ['NOUN','anim','masc','Name','plur','ablt'])

    test = Word.Tags('козе')
    Test.Add(service+'.Tags','normal 2', test, ['NOUN','anim','femn','sing','datv'])
    
    test = Word.Tags('Два слова')
    Test.Add(service+'.Tags','unreal 1', test, ['NOUN','inan','neut','sing','gent'])

    test = Word.Tags(' ')
    Test.Add(service+'.Tags','unreal 2', test, [])

    test = Word.Tags(5)
    Test.Add(service+'.Tags','crash', test, [])


    # LangDetect
    test = String.LangDetect('Табареками')
    Test.Add(service+'.LangDetect','normal 1', test, 'русский')

    # Translit
    test = Modif.Translit('Turaabad')
    Test.Add(service+'.Translit','normal 1', test, 'Тураабад')

    test = Modif.Translit('Shyukyurbeyli')
    Test.Add(service+'.Translit','normal 2', test, 'Шукюрбейли')

print('')
print('------- Отчёт тестов сервиса %s --------' % service)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % service)
print(Report.WriteFails())
