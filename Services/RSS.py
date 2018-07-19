# -*- coding: utf-8 -*-
import feedparser
import Fixer

# обработка абзацев
def formatting(text):
    text = text.replace('<br>','\n')
    text = text.replace('\n\n','\n')
    return text

# Получить весь RSS
def GetRSS(urlRSS):
    try:
        d = feedparser.parse(urlRSS)
        if d['version'] == '': d['version'] = '#problem: no RSS'
        return d
    except:
        Fixer.errlog('RSS.GetRSS', str(e))
        d['version'] = '#bug: no URL'
        return d

# Класс для парсинга RSS-лент
class RSS:

    # Получить заголовки RSS
    def GetHeaders(urlRSS):
        d = GetRSS(urlRSS)
        if d['version'][0] == '#': return {'status': d['version']}
        return d.headers

    # Получить дату последней публикации
    def GetDate(urlRSS):
        d = GetRSS(urlRSS)
        if d['version'][0] == '#': return d['version']
        return d['feed']['updated']

    # Получить только оглавление
    def GetTitles(urlRSS):
        d = GetRSS(urlRSS)
        if d['version'][0] == '#': return {'status': d['version']}
        dtitles = {'status': 'ok'}
        dtitles['title'] = d.feed.title
        if 'subtitle' in d['feed']: dtitles['subtitle'] = d.feed.subtitle
        else: dtitles['subtitle'] = d.feed.title
        dtitles['link'] = d.feed.link
        if 'author' in d['feed']: dtitles['author'] = d.feed.author
        else: dtitles['author'] = 'Не указан'
        if 'language' in d['feed']: dtitles['lang'] = d.feed.language
        else: dtitles['lang'] = 'none'
        if 'updated' in d['feed']: dtitles['date'] = d.feed.updated
        elif 'published' in d['feed']: dtitles['date'] = d.feed.published
        else: dtitles['date'] = 'Не указана'
        return dtitles

    # Получить оглавление и часть постов (0 - все посты)
    def GetFeed(urlRSS, items=0):
        d = GetRSS(urlRSS)
        if d['version'][0] == '#': return d['version']
        stext = '%s\n%s\n' % (d.feed.title, d.feed.subtitle)
        Fixer.htext = d['feed']['link']
        i = len(d['entries'])
        if i < items: items = i
        if items == 0: items = i
        for item in range(0, items-1):
            post = d.entries[item]
            sdesc = ''
            if 'description' in post: sdesc = formatting(post.description)
            stext += '\n%s\n%s\n' % (post.title, sdesc)
        return stext

    # Получить отдельный пост (с заголовком или нет)
    def GetPost(urlRSS, item=0, btitle=True, bdate=False):
        d = GetRSS(urlRSS)
        if d['version'][0] == '#': return d['version']
        i = len(d['entries'])-1
        if i < item: item = i
        post = d.entries[item]
        Fixer.htext = post.link
        sdate = ''
        if bdate: sdate = '\n' + post.published
        sdesc = ''
        if 'description' in post: sdesc = formatting(post.description)
        if btitle:
            return '%s : %s\n%s' % (d.feed.title, post.title, sdesc)+sdate
        else: return sdesc + sdate

    # Получить все посты в виде dict
    def GetPosts(urlRSS):
        d = GetRSS(urlRSS)
        if d['version'][0] == '#': return {'status': d['version']}
        posts = []
        for post in d.entries:
            dpost = {}
            dpost['title'] = post.title
            if 'description' in post: dpost['description'] = formatting(post.description)
            else: dpost['description'] = post.title
            dpost['len'] = len(dpost['description'])
            dpost['link'] = post.link
            dpost['date'] = post.published
            posts.append(dpost)
        return posts

    # Получить только новые посты в виде dict
    def GetNewPosts(urlRSS, oldposts):
        d = GetRSS(urlRSS)
        if d['version'][0] == '#': return {'status': d['version']}
        posts = []
        for post in d.entries:
            dpost = {}
            dpost['title'] = post.title
            if 'description' in post: dpost['description'] = formatting(post.description)
            else: dpost['description'] = post.title
            dpost['link'] = post.link
            dpost['date'] = post.published
            # проверка
            bapp = True
            for opost in oldposts:
                if dpost['date'] == opost['date'] and len(dpost['description']) == opost['len']: bapp = False # если совпало 
            if bapp: posts.append(dpost) # добавлять, если не найдено совпадений
        return posts
