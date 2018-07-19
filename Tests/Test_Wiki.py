import Fixer
import wikipedia
from Services.Geo import Geo
#import SMath

wikipedia.set_lang('ru')

class Wiki:
    # Поиск страниц по заданному названию
    def SearchPage(sname, resnum = 10):
        #try:
            rez = []
            if sname == '': return rez
            rez = wikipedia.search(sname, results = resnum)
            return rez

    # Весь текстовый контент статьи
    def FullContent(spage):
        #try:
            rez = wikipedia.page(spage)
            if rez.content == '': return '#problem: 404'
            text = rez.content #.encode('utf8')
            return text

    # Вся информация о статье по типу: content, categories, coordinates, html, images, links
    def Page(spage, stype='summary'):
        #try:
            rez = wikipedia.page(spage)
            if stype == 'content': return rez.content
            elif stype == 'categories': return rez.categories
            elif stype == 'coordinates': return rez.coordinates
            elif stype == 'html': return rez.html
            elif stype == 'images': return rez.images
            elif stype == 'links': return rez.links
            elif stype == 'references': return rez.references
            elif stype == 'sections': return rez.sections
            return rez.summary
    
    # Минимальный контент статьи - первый абзац
    def MiniContent(spage):
        #try:
            rez = wikipedia.page(spage)
            if rez.content == '': return '#problem: 404'
            num = rez.content.find('\n==')
            text = rez.content[0:num] #.encode('utf8')
            return text     

    # Произвольная статья в Wikipedia
    def PageRandom():
        #try:
            rez = wikipedia.random()
            return Wiki.MiniContent(rez[0])

    # Найти объекты wiki поблизости от location (x, y)
    def GeoSearch(x,y,resnom=10,rad=1000):
        #try:
            rez = wikipedia.geosearch(y, x, title=None, results=resnom, radius=rad)
            if len(rez) == 0: return '#problem: no objects'
            return rez

    # Найти ближайший объект wiki поблизости от location (x, y) - возвращает MiniContent
    def GeoFirst(x,y,rad=1000):
        #try:
            rez = wikipedia.geosearch(y, x, title=None, results=10, radius=rad)
            if len(rez) == 0: return 'В радиусе '+str(rad)+'метров не найдено ни одного интересного объекта!'
            for ip in rez:
                try:
                    irez = wikipedia.page(ip)
                    dist = int(1000 * Geo.Distance(irez.coordinates[1], irez.coordinates[0], x, y))
                    return 'Найден ближайший объект в '+str(dist)+' метрах.\n' + Wiki.MiniContent(rez[1])
                except: # не удалось загрузить страницу
                    continue
            return 'Не удалось загрузить информацию :('

    def GeoFirstMe(rad=1000):
        #try:
            return Wiki.GeoFirst(Fixer.X, Fixer.Y, rad=rad)


print('Тестирование Wiki...')
print(Wiki.GeoFirstMe())
#test = input('Введите строку поиска: ')
#etype = input('Введите категорию: ')
#print(Wiki.Page(test, etype))
