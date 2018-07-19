import Fixer
from DB.SQLite import SQL

def AddTable(NameTable, dCols, data):
    print('Создание таблицы "%s"' % NameTable)
    print('Результат: ' + SQL.Table(NameTable, dCols))
    print('Запись данных: %i строк' % len(data))
    print('Результат: ' + SQL.WriteBlock(NameTable, data))
    print('-------------------------------------')

# основной блок программы
#----------------------------------

yn = input('...... Создать таблицы и загрузить данные? Y/N: ')
if yn == 'Y': 

    # База имён

    mNames = []
    for iname in Fixer.Names:
        mRow = []
        mRow.append(iname)
        iSex = 0
        if Fixer.Names[iname][0]: iSex = 1
        mRow.append(iSex)
        mRow.append(Fixer.Names[iname][1])
        mRow.append(Fixer.Names[iname][2])
        mRow.append(iname.upper().replace('Ё','Е'))
        mNames.append(mRow)
    AddTable('names', {'name': 'text nn u', 'sex': 'int', 'summ': 'int', 'country': 'text',
                       'nameU': 'text nn'}, mNames)

    # База анекдотов

    db = []
    try:
        f = open('DB/anecdotes.txt', encoding='utf-8')
        for line in f:
            db.append(line.replace('\\','\n'))
        f.close()
    except Exception as e:
        Fixer.errlog('Fun', 'Ошибка при загрузке базы anecdotes!: ' + str(e))

    mAnecs = []
    i = 0
    for item in db:
        mRow = []
        mRow.append(i)
        mRow.append(0)
        mRow.append(item)
        mRow.append(item.upper().replace('Ё','Е'))
        mAnecs.append(mRow)
        i += 1
    AddTable('anecdotes', {'id': 'int kp nn u', 'type': 'int', 'text': 'text nn', 'textU': 'text nn'}, mAnecs)

    # База комплиментов

    mCompliment = []
    wCompliment = []
    try:
        i = 0
        f = open('DB/mCompliment.txt', encoding='utf-8')
        for line in f:
            m = []
            m.append(i)
            m.append(line.replace('\n',''))
            mCompliment.append(m)
            i += 1
        f.close()
        i = 0
        f = open('DB/wCompliment.txt', encoding='utf-8')
        for line in f:
            m = []
            m.append(i)
            m.append(line.replace('\n',''))
            wCompliment.append(m)
            i += 1
        f.close()
    except Exception as e:
        errlog('compliments', 'Ошибка при загрузке комплиментов: ' + str(e))

    AddTable('complimentMen', {'id':'int pk nn u','text':'text nn'}, mCompliment)
    AddTable('complimentWoman', {'id':'int pk nn u','text':'text nn'}, wCompliment)

    # База валют

    mval = []
    for kval in Fixer.Valutes:
        m = []
        m.append(kval)
        m.append(Fixer.Valutes[kval])
        mval.append(m)
    AddTable('valutes', {'code':'text nn u','name':'text nn'}, mval)

    mval = []
    for kval in Fixer.valutes:
        m = []
        m.append(kval)
        m.append(Fixer.valutes[kval])
        mval.append(m)
    AddTable('valutes2', {'code':'text nn u','name':'text nn'}, mval)    

    # База городов/станций

    i = 0
    try:
        f = open('DB/stations.txt', encoding='utf-8')
        db = []
        for line in f:
            m = []
            words = line.strip().split(' : ')
            words.append(words[0])
            words.append(words[1])
            words.append(words[2])
            words.append(words[3])
            if words[4] == '': words[8] = words[8][3:]
            else: words[8] = words[8][4:]
            words[0] = words[0].upper() + ' '
            words[0] = words[0].replace('Ё','Е')
            words[1] = words[1].upper()
            words[1] = words[1].replace('Ё','Е')
            words[2] = words[2].upper()
            words[2] = words[2].replace('Ё','Е')
            words[3] = words[3].upper()
            words[3] = words[3].replace('Ё','Е')
            m.append(i)
            m.append(words[8])
            m.append(words[9])
            m.append(words[10])
            m.append(words[11])
            m.append(words[4])
            m.append(words[5])
            m.append(words[6])
            m.append(words[7])
            m.append(words[0])
            m.append(words[1])
            m.append(words[2])
            m.append(words[3])
            db.append(m)
            i += 1
        f.close()
        AddTable('stations', {'id':'int pk nn u','name':'text nn',
                              'city':'text','region':'text',
                              'country':'text',
                              'type':'text',
                              'y':'real','x':'real','code':'text nn',
                              'nameU':'text nn','cityU':'text',
                              'regionU':'text','countryU':'text'}, db)
    except:
        print(i)

    # база сайтов (Яндекс.Каталог)

    i = 0
    try:
        f = open('DB/YandexCatalog.csv', encoding='utf-8')
        yacat = []
        for line in f:
            m = []
            words = line.split(';')
            m.append(i)
            for item in range(0,len(words)):
                m.append(words[item])
            words[1] = words[1].upper().replace('Ё','Е')
            m.append(words[1])
            words[9] = words[9].upper().replace('Ё','Е')
            m.append(words[9])
            yacat.append(m)
            i += 1
        f.close()
        del(yacat[0])
        print(yacat[0])
        AddTable('yaCatalog', {'id':'int pk nn u','site':'text nn',
                              'title':'text nn','tic':'int',
                              'section':'text','section2':'text',
                              'section3':'text','section4':'text',
                              'section5':'text','section6':'text',
                              'regionRu':'text','region':'text','region2':'text',
                              'region3':'text','region4':'text',
                              'titleU':'text nn','regionRuU':'text'}, yacat)
    except Exception as e:
        Fixer.errlog('Yandex.Каталог', 'Ошибка при загрузке YandexCatalog.csv!: ' + str(e))

    # База языков

    dir_lang = ["az-ru", "be-bg", "be-cs", "be-de", "be-en", "be-es", "be-fr", "be-it", "be-pl", "be-ro", "be-ru", "be-sr", "be-tr", "bg-be", "bg-ru", "bg-uk", "ca-en", "ca-ru", "cs-be", "cs-en", "cs-ru", "cs-uk", "da-en", "da-ru", "de-be", "de-en", "de-es", "de-fr", "de-it", "de-ru", "de-tr", "de-uk", "el-en", "el-ru", "en-be", "en-ca", "en-cs", "en-da", "en-de", "en-el", "en-es", "en-et", "en-fi", "en-fr", "en-hu", "en-it", "en-lt", "en-lv", "en-mk", "en-nl", "en-no", "en-pt", "en-ru", "en-sk", "en-sl", "en-sq", "en-sv", "en-tr", "en-uk", "es-be", "es-de", "es-en", "es-ru", "es-uk", "et-en", "et-ru", "fi-en", "fi-ru", "fr-be", "fr-de", "fr-en", "fr-ru", "fr-uk", "hr-ru", "hu-en", "hu-ru", "hy-ru", "it-be", "it-de", "it-en", "it-ru", "it-uk", "lt-en", "lt-ru", "lv-en", "lv-ru", "mk-en", "mk-ru", "nl-en", "nl-ru", "no-en", "no-ru", "pl-be", "pl-ru", "pl-uk", "pt-en", "pt-ru", "ro-be", "ro-ru", "ro-uk", "ru-az", "ru-be", "ru-bg", "ru-ca", "ru-cs", "ru-da", "ru-de", "ru-el", "ru-en", "ru-es", "ru-et", "ru-fi", "ru-fr", "ru-hr", "ru-hu", "ru-hy", "ru-it", "ru-lt", "ru-lv", "ru-mk", "ru-nl", "ru-no", "ru-pl", "ru-pt", "ru-ro", "ru-sk", "ru-sl", "ru-sq", "ru-sr", "ru-sv", "ru-tr", "ru-uk", "sk-en", "sk-ru", "sl-en", "sl-ru", "sq-en", "sq-ru", "sr-be", "sr-ru", "sr-uk", "sv-en", "sv-ru", "tr-be", "tr-de", "tr-en", "tr-ru", "tr-uk", "uk-bg", "uk-cs", "uk-de", "uk-en", "uk-es", "uk-fr", "uk-it", "uk-pl", "uk-ro", "uk-ru", "uk-sr", "uk-tr"]
    langs = {"АФРИКААНС":"af","АМХАРСКИЙ":"am","АРАБСКИЙ":"ar","АЗЕРБАЙДЖАНСКИЙ":"az","БАШКИРСКИЙ":"ba","БЕЛОРУССКИЙ":"be","БОЛГАРСКИЙ":"bg","БЕНГАЛЬСКИЙ":"bn","БОСНИЙСКИЙ":"bs","КАТАЛАНСКИЙ":"ca","СЕБУАНСКИЙ":"ceb","ЧЕШСКИЙ":"cs","ВАЛЛИЙСКИЙ":"cy","ДАТСКИЙ":"da","НЕМЕЦКИЙ":"de","ГРЕЧЕСКИЙ":"el","ЭМОДЗИ":"emj","АНГЛИЙСКИЙ":"en","ЭСПЕРАНТО":"eo","ИСПАНСКИЙ":"es","ЭСТОНСКИЙ":"et","БАСКСКИЙ":"eu","ПЕРСИДСКИЙ":"fa","ФИНСКИЙ":"fi","ФРАНЦУЗСКИЙ":"fr","ИРЛАНДСКИЙ":"ga","ШОТЛАНДСКИЙ (ГЭЛЬСКИЙ)":"gd","ГАЛИСИЙСКИЙ":"gl","ГУДЖАРАТИ":"gu","ИВРИТ":"he","ХИНДИ":"hi","ХОРВАТСКИЙ":"hr","ГАИТЯНСКИЙ":"ht","ВЕНГЕРСКИЙ":"hu","АРМЯНСКИЙ":"hy","ИНДОНЕЗИЙСКИЙ":"id","ИСЛАНДСКИЙ":"is","ИТАЛЬЯНСКИЙ":"it","ЯПОНСКИЙ":"ja","ЯВАНСКИЙ":"jv","ГРУЗИНСКИЙ":"ka","КАЗАХСКИЙ":"kk","КХМЕРСКИЙ":"km","КАННАДА":"kn","КОРЕЙСКИЙ":"ko","КИРГИЗСКИЙ":"ky","ЛАТЫНЬ":"la","ЛЮКСЕМБУРГСКИЙ":"lb","ЛАОССКИЙ":"lo","ЛИТОВСКИЙ":"lt","ЛАТЫШСКИЙ":"lv","МАЛАГАСИЙСКИЙ":"mg","МАРИЙСКИЙ":"mhr","МАОРИ":"mi","МАКЕДОНСКИЙ":"mk","МАЛАЯЛАМ":"ml","МОНГОЛЬСКИЙ":"mn","МАРАТХИ":"mr","ГОРНОМАРИЙСКИЙ":"mrj","МАЛАЙСКИЙ":"ms","МАЛЬТИЙСКИЙ":"mt","БИРМАНСКИЙ":"my","НЕПАЛЬСКИЙ":"ne","ГОЛЛАНДСКИЙ":"nl","НОРВЕЖСКИЙ":"no","ПАНДЖАБИ":"pa","ПАПЬЯМЕНТО":"pap","ПОЛЬСКИЙ":"pl","ПОРТУГАЛЬСКИЙ":"pt","РУМЫНСКИЙ":"ro","РУССКИЙ":"ru","СИНГАЛЬСКИЙ":"si","СЛОВАЦКИЙ":"sk","СЛОВЕНСКИЙ":"sl","АЛБАНСКИЙ":"sq","СЕРБСКИЙ":"sr","СУНДАНСКИЙ":"su","ШВЕДСКИЙ":"sv","СУАХИЛИ":"sw","ТАМИЛЬСКИЙ":"ta","ТЕЛУГУ":"te","ТАДЖИКСКИЙ":"tg","ТАЙСКИЙ":"th","ТАГАЛЬСКИЙ":"tl","ТУРЕЦКИЙ":"tr","ТАТАРСКИЙ":"tt","УДМУРТСКИЙ":"udm","УКРАИНСКИЙ":"uk","УРДУ":"ur","УЗБЕКСКИЙ":"uz","ВЬЕТНАМСКИЙ":"vi","КОСА":"xh","ИДИШ":"yi","КИТАЙСКИЙ":"zh"}

    dirlangs = []
    for lang in dir_lang:
        m = []
        m.append(lang[:2])
        m.append(lang[3:])
        dirlangs.append(m)
    AddTable('yaDirLang', {'langFrom':'char(2) nn','langTo':'char(2) nn'}, dirlangs)

    yalangs = []
    for klang in langs:
        m = []
        m.append(klang)
        m.append(langs[klang])
        yalangs.append(m)
    AddTable('yaLangs', {'lang':'text pk nn u','code':'char(2) nn'}, yalangs)

    # база IATA

    i = 0
    try:
        f = open('DB/IATA.txt', encoding='utf-8')
        db = []
        for line in f:
            m = []
            words = line.split(' : ')
            m.append(i)
            for item in range(0, len(words)):
                m.append(words[item].strip())
            words[1] = words[1].upper() + ' '
            words[1] = words[1].replace('Ё','Е')
            m.append(words[1])
            db.append(m)
            i += 1
        f.close()
        del(db[0])
        print(db[0])
        AddTable('IATA', {'id':'int pk nn u','code':'char(4) nn u','city':'text nn','cityEn':'text','regionCode':'char(2)',
                              'countryCode':'char(2)','iataCode':'char(3)','ikaoCode':'char(4)','cityU':'text nn'}, db)
    except:
        print(i)

    # база IATA аэропортов

    i = 0
    try:
        f = open('DB/IATA.csv', encoding='utf-8')
        db = []
        for line in f:
            m = []
            words = line.split('|')
            m.append(i)
            for item in range(0, len(words)):
                if item % 2 == 0:
                    m.append(words[item].strip())
            words[4] = words[4].upper() + ' '
            words[4] = words[4].replace('Ё','Е')
            m.append(words[4])
            words[8] = words[8].upper() + ' '
            words[8] = words[8].replace('Ё','Е')
            m.append(words[8])
            db.append(m)
            i += 1
        f.close()
        print(db[0])
        AddTable('IATA_airports', {'id':'int pk nn u','code':'char(4) nn u','ikaoCode':'char(4)',
                          'name':'text','nameEng':'text','cityName':'text',
                          'cityNameEng':'text','timeZone':'float',
                          'country':'text','countryEng':'text','lat':'float','lon':'float',
                          'runwayLength':'int','runwayElevation':'int',
                          'phone':'text','email':'text','website':'text',
                          'nameU':'text','cityNameU':'text'}, db)
    except Exception as e:
        print(str(e))
