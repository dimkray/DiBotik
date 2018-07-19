# Обновление базы данных ЕГР из открытых источников
import csv
import Fixer
from DB.SQLite import SQL, CSV
from DB.Worker import Worker
from Services.StrMorph import Word, Modif

Fixer.DB = 'DB/Geo.db'

# основной блок программы
#----------------------------------

items = 100000
block = 1000000

yn = input('...... Обновить таблицы БД и загрузить новые данные? Y/N: ')
if yn != 'N': 

    # Словари
##    Worker.UpdateTableCSV('E:/SQL/Cities/countryInfo.txt', 'countries',
##        {'iso': 'text pk nn u', 'iso3': 'text', 'iso_numeric': 'text', 'fips': 'text', 'name': 'text', 'capital': 'text', 'area': 'float',
##         'population': 'int', 'continent': 'text', 'tld': 'text', 'currency_code': 'text',
##         'currency_name': 'text', 'phone': 'text', 'postcode_format': 'text', 'postcode_regex': 'text',
##         'languages': 'text', 'geo_id': 'int', 'neighbours': 'int', 'equivalent_fipscode': 'text'}, separator='\t', symb='"')
    Worker.UpdateTableCSV('E:/SQL/Cities/iso-languagecodes.txt', 'languages',
        {'iso3': 'text pk nn u', 'iso2': 'text', 'iso1': 'text', 'name': 'text'}, separator='\t', symb='"')
    Worker.UpdateTableCSV('E:/SQL/Cities/featureCodes_ru.txt', 'feature_codes',
        {'code': 'text pk nn u', 'name': 'text', 'description': 'text'}, separator='\t', symb='"')
    dType = Worker.DictionaryCSV('E:/SQL/Cities/featureCodes_ru.txt', keycol='code', mCols=['name'], separator='\t', symb='"')

    dAdmin1 = Worker.DictionaryCSV('E:/SQL/Cities/admin1Codes.txt', keycol='code', mCols=['geo_id'], separator='\t', symb='"')
    dAdmin2 = Worker.DictionaryCSV('E:/SQL/Cities/admin2Codes.txt', keycol='code', mCols=['geo_id'], separator='\t', symb='"')

    Worker.ReadBlockCSV('E:/SQL/Cities/timeZones.txt', separator='\t', symb='"')
    dTimeZones = {} # заполнения словаря timeZones
    for row in Worker.mDataCSV:
        m = []
        m.append(row[2])
        m.append(row[3])
        m.append(row[4])
        dTimeZones[row[0]+'.'+row[1]] = m

    # Таблица названий объектов

    dName = {}; dLink = {}
    # ['abbr' - аббревиатура,'icao' - ICAO,'link' - ссылка,'post' - почта,'wkdt' - ?]
    for ib in range(0, 13):
        Worker.ReadBlockCSV('E:/SQL/Cities/alternateNamesV2.txt', iblock=ib, separator='\t')
        Worker.mTableCSV = Fixer.inList(Worker.mTableCSV, 'Params')
        irow = 0
        for row in Worker.mDataCSV:
            if (row[2] == 'ru' or row[2] == None) and row[3] is not None:
                if row[5] is None and row[6] is None and row[7] is None:
                    iType = Word.Type(row[3])
                    if iType != 0 and iType != 50:
                        dName[row[1]] = row[3]
            if row[2] == 'link': dLink[row[1]] = row[3]
            sparams = ''
            if row[4] is not None: sparams += 'p' # isPreferredName
            if row[5] is not None: sparams += 's' # isShortName
            if row[6] is not None: sparams += 'c' # isColloquial
            if row[7] is not None: sparams += 'h' # isHistoric
            row.append(sparams)
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))
        Worker.UpdateBlockCSV('names', {
            'geo_id': 'int nn', 'iso': 'text', 'name': 'text nn',
            'params': 'text' },
            {'geo_id': 'geonameid', 'iso': 'isolanguage', 'name': 'alternate name',
            'params': 'Params'})
    Worker.Indexation('names', ['geo_id', 'name'])

    # Таблица городов

    for ib in range(0, 12):
        Worker.ReadBlockCSV('E:/SQL/Cities/allCountries.txt', iblock=ib, separator='\t', symb='"')
        irow = 0
        Worker.mTableCSV = Fixer.inList(Worker.mTableCSV, 'type')
        Worker.mTableCSV = Fixer.inList(Worker.mTableCSV, 'link')
        Worker.mTableCSV = Fixer.inList(Worker.mTableCSV, 'name_ru')
        Worker.mTableCSV = Fixer.inList(Worker.mTableCSV, 'nameU_ru')
        Worker.mTableCSV = Fixer.inList(Worker.mTableCSV, 'tz')
        Worker.mTableCSV = Fixer.inList(Worker.mTableCSV, 'tile')
        for row in Worker.mDataCSV:
            try:
                if row[6] is not None and row[7] is not None:
                    idType = row[6]+'.'+row[7]
                    if idType in dType: # Тип объекта
                        row.append(dType[idType])
                    else:
                        row.append(None)
                else:
                    row.append(None)
                if row[0] in dLink: # Link
                    row.append(dLink[row[0]])
                else:
                    row.append(None)
                name = None
                if row[0] in dName: # Русское наименование
                    name = dName[row[0]]
                else:
                    if row[2] is not None:
                        name = Modif.Translit(row[2])
                row.append(name)
                if name is not None:
                    row.append(name.upper().replace('Ё','Е'))
                else:
                    row.append(None)
                if row[8] is not None and row[10] is not None:
                    admin1 = row[8]+'.'+row[10]
                    if admin1 in dAdmin1:
                        row[10] = dAdmin1[admin1]
                if row[8] is not None and row[11] is not None:
                    admin2 = row[8]+'.'+row[11]
                    if admin2 in dAdmin2:
                        row[11] = dAdmin2[admin2]
                if row[8] is not None and row[17] is not None:
                    timeZone = row[8]+'.'+row[17]
                    if timeZone in dTimeZones:
                        row.append(dTimeZones[timeZone][2])
                    else:
                        row.append(None)
                else:
                    row.append(None)
                # Создаём tile
                stile = None
                if row[4] is not None and row[5] is not None:
                    lat = float(row[4])
                    lon = float(row[5])
                    dcLat = (lat - int(lat)) * 10
                    dcLon = (lon - int(lon)) * 10
                    stile = '%i,%i|%i,%i' % (int(lat), int(lon), int(dcLat), int(dcLon))
                row.append(stile)
            except Exception as e:
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                print('!!! BUG - ' + str(e))
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))
        Worker.UpdateBlockCSV('cities', {
            'id': 'int pk nn u', 'name': 'text nn', 'name_ascii': 'text', 'name_ru': 'text', 'link': 'text', # 'name_alternate': 'text',
            'lat': 'float', 'lon': 'float', 'tile': 'text', 'feature_class': 'text', 'feature_code': 'text', 'type': 'text',
            'country_code': 'text', 'code1': 'text', 'code2': 'text',
            'code3': 'text', 'code4': 'text', 'population': 'int', 'elevation': 'int',
            'timezone': 'text', 'tz': 'float', 'date': 'text', 'nameU_ru': 'text'}, # 'dem': 'int'
            {'id': 'geonameid', 'name': 'name', 'name_ascii': 'asciiname', 'name_ru': 'name_ru', 'link': 'link',
            'lat': 'latitude', 'lon': 'longitude', 'tile': 'tile',
            'feature_class': 'feature class', 'feature_code': 'feature code', 'type': 'type',
            'country_code': 'country code', 'code1': 'admin1 code', 'code2': 'admin2 code',
            'code3': 'admin3 code', 'code4': 'admin4 code', 'population': 'population', 'elevation': 'elevation',
            'timezone': 'timezone', 'tz': 'tz', 'date': 'modification date', 'nameU_ru': 'nameU_ru'})
    Worker.Indexation('cities', ['id', 'name_ascii', 'nameU_ru', 'tile', 'code1', 'code2', 'population'])
        
