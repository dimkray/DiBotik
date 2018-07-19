# -*- coding: utf-8 -*-
# Сервис морфологического анализа
import re
import Fixer
import pymorphy2

dic = Fixer.Load('morth') # словарь морфологических определений
morph = pymorphy2.MorphAnalyzer()

phr = {'NOUN': 1,  # существительное
       'ADJF': 2,  # прилагательное (полное)
       'ADJS': 3,  # прилагательное (краткое)
       'COMP': 4,  # компаратив
       'VERB': 5,  # глагол (личная форма)
       'INFN': 6,  # глагол (инфинитив)
       'PRTF': 7,  # причастие (полное)
       'PRTS': 8,  # причастие (краткое)
       'GRND': 9,  # деепричастие
       'NUMR': 10, # числительное
       'ADVB': 11, # наречие
       'NPRO': 12, # местоимение
       'PRED': 13, # предикатив
       'PREP': 14, # предлог
       'CONJ': 20, # союз
       'PRCL': 15, # частица
       'INTJ': 16, # междометие
       'NUMB': 40, # номер/цифра
       'ROMN': 45, # римская цифра
       'LATN': 50, # латиница
       'PNCT': 90, # знак пунктуации
       'UNKN': 0 } # неизвестное

ccltkr = {'shch': 'щ', 'you': 'ю', 'rth': 'рф', 'tion': 'шен', 'ath': 'aф',
          'thi': 'фи', 'the': 'фе', 'nee': 'ни', 'bee': 'би', 'ree': 'ри',
          'pha': 'фа', 'qua': 'ква'}

cltkr = {'ya': 'я', 'ye': 'е', 'yo': 'йо', 'yu': 'ю',
         'ja': 'я', 'je': 'е', 'jo': 'ё', 'ju': 'ю', 
         'ch': 'ч', 'sh': 'ш', 'kh': 'х', 'zh': 'ж',
         'ts': 'ц', 'tz': 'ц', 'cz': 'ч', 'sz': 'ш',
         'ay': 'ай', 'ey': 'ей', 'iy': 'ий', 'oy': 'ой', 'uy': 'уй', 'yy': 'ый', 
         'ai': 'ай', 'ei': 'ей', 'oi': 'ой',
         'ie': 'е',
         'ej': 'ей', 'aj': 'ай', 'oj': 'ой', 'uj': 'уй',
         'zw': 'цв'}

ltkr = {'a': 'а', 'b': 'б', 'c': 'ц', 'd': 'д',
        'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'х',
        'i': 'и', 'j': 'дж', 'k': 'к', 'l': 'л',
        'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
        'q': 'к', 'r': 'р', 's': 'с', 't': 'т',
        'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кс',
        'y': 'ы', 'z': 'з', '\'': 'ь', '"': 'ъ'}

krlt = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'\'','ы':'y','ь':'\'','э':'e',
      'ю':'u','я':'ja'}

# Получение отдельных предложений
def Strings(text):
    try:
        text = text.replace('	','  ') # учитываем табы
        if text.strip() == '': return []
        poz = 0; newpoz = 0
        mstr = [] # массив предложений
        while newpoz <= len(text):
            x1 = 0; x2 = 0; x3 = 0; x4 = 0
            if text.find('. ', poz) > 0: x1 = text.find('. ', poz)
            else: x1 = 1000000
            if text.find('! ', poz) > 0: x2 = text.find('! ', poz)
            else: x2 = 1000000
            if text.find('? ', poz) > 0: x3 = text.find('? ', poz)
            else: x3 = 1000000
            if text.find('\n', poz) > 0: x4 = text.find('\n', poz)
            else: x4 = 1000000    
            newpoz = min(x1, x2, x3, x4) + 1 # Ищем ближайший разделитель предложения
            s = text[poz:newpoz].strip()
            if s != '': mstr.append(s)
            poz = newpoz
        return mstr # возвращаем отдельные предложения
    except Exception as e:
        Fixer.errlog('StrMorph.Strings', str(e))
        return []

# Получение отдельных слов из строки и получение конструкции строки
def Words(strtext):
    try:
        if strtext.strip() == '': return [], strtext
        words = re.split('\s|/|\\|\*|"|`|<|>|\]|\[|\}|\{|=|\+|\)|\(|&|\^|#|\~|@|»|«|:|;|,|\.|!|\?|-', strtext)
        mwords = [] # массив слов
        text = ''
        poz = 0; pozold = 0
        for word in words:
            s = word.strip()
            if s != '' and s != '-' and s != '—':
                poz = strtext.find(word,poz)
                text += strtext[pozold:poz] + '[' + s + ']'
                poz += len(word); pozold = poz
                mwords.append(s)
        text += strtext[poz:] # окончание предложения
        return mwords, text # возвращаем отдельные слова и конструкцию слов в запросе
    except Exception as e:
        Fixer.errlog('StrMorph.Words', str(e))
        return [], strtext

# Получение морфологического анализатора
def GetMorth(word):
    if word.strip() == '': return ''
    word = word.strip().lower() # доработка слова
    p = morph.parse(word)[0]
    return p

# --------------------------------------------------------------
# Основной класс по работе со строковыми запросами
class String:
    # Количество предложений в запросе
    def StringsCount(text):
        return len(Strings(text))
        
    # Получение всех предложений
    def GetStrings(text):
        return Strings(text)

    # Количество слов в запросе
    def WordsCount(text):
        mwords, constr = Words(text)
        return len(mwords)
        
    # Получение всех отдельных слов из запроса
    def GetWords(text):
        mwords, constr = Words(text)
        return mwords

    # Получение конструкции слов запроса
    def GetConstr(text):
        mwords, constr = Words(text)
        return constr

# Основной класс по работе со словами
class Word:
    # Получение тэгов по морфологическому анализу слова
    def Tags(word):
        try:
            if word.strip() == '': return []
            p = GetMorth(word)
            print(p)
            mtags = re.split(',| ', str(p.tag))
            return mtags
        except Exception as e:
            Fixer.errlog('StrMorph.Tags', str(e))
            return []

    # Получение морфологического анализа слова
    def Morph(word):
        p = GetMorth(word)
        smorth = '%s - [%s]' % (word, p.normal_form)
        mtags = re.split(',| ', str(p.tag))
        for tag in mtags:
            if dic[tag][1] != '': s = ' {%s}' % dic[dic[tag][1]][0]
            smorth += '\n - ' + dic[tag][0] + s
        return smorth + '\n'

    # Получение нормальной формы слова
    def Normal(word):
        if word.strip() == '': return ''
        word = word.strip().lower() # доработка слова
        p = morph.parse(word)[0]
        return p.normal_form
    
    # Получение типа слова (константа) - см phr
    def Type(word): 
        p = GetMorth(word)
        mtags = re.split(',| ', str(p.tag))
        for tag in mtags:
            if dic[tag][1] == 'POST':
                if tag in phr:
                    return phr[tag]
                else:
                    return 0
        return 0

    # Получение части речи
    def TagPart(word): 
        p = GetMorth(word)
        if p.tag.POS is not None: return p.tag.POS
        else: 'NONE'

    # Получение признака одушевлённости
    def TagAnimacy(word): 
        p = GetMorth(word)
        if p.tag.animacy is not None: return p.tag.animacy
        else: 'NONE'

    # Получение вида: совершенный или несовершенный
    def TagAspect(word): 
        p = GetMorth(word)
        if p.tag.aspect is not None: return p.tag.aspect
        else: 'NONE'

    # Получение падежа
    def TagCase(word): 
        p = GetMorth(word)
        if p.tag.case is not None: return p.tag.case
        else: 'NONE'

    # Получение рода: мужской, женский, средний
    def TagGender(word): 
        p = GetMorth(word)
        if p.tag.gender is not None: return p.tag.gender
        else: 'NONE'

    # Включённость говорящего в действие
    def TagInv(word): 
        p = GetMorth(word)
        if p.tag.involvement is not None: return p.tag.involvement
        else: 'NONE'

    # Получение наклонения: повелительное, изъявительное
    def TagMood(word): 
        p = GetMorth(word)
        if p.tag.mood is not None: return p.tag.mood
        else: 'NONE'

    # Получение числа: единственное, множественное
    def TagNumber(word): 
        p = GetMorth(word)
        if p.tag.number is not None: return p.tag.number
        else: 'NONE'

    # Получение лица: первое, второе, третье
    def TagPerson(word): 
        p = GetMorth(word)
        if p.tag.person is not None: return p.tag.person
        else: 'NONE'

    # Получение времени: настоящее, прошедшее, будущее
    def TagTense(word): 
        p = GetMorth(word)
        if p.tag.tense is not None: return p.tag.tense
        else: 'NONE'

    # Получение переходности: переходный, непереходный
    def TagTrans(word): 
        p = GetMorth(word)
        if p.tag.transitivity is not None: return p.tag.transitivity
        else: 'NONE'

    # Получение залога: действительный, страдательный
    def TagVoice(word): 
        p = GetMorth(word)
        if p.tag.voice is not None: return p.tag.voice
        else: 'NONE'

    # Склонение слов
    def inflect(word, dinflect={'nomn'}): # по умолчанию в именительный падеж
        p = GetMorth(word)
        try:
            p = p.inflect(dinflect)
            return p.word
        except e as Exception:
            Fixer.errlog('StrMorth.inflect', str(e))
            return word

# Класс модификации текста
class Modif:
    
    # транслитерация текста
    def Translit(text, bToRus=True):
        try: 
            mWordUpper = []
            mWords = String.GetWords(text)
            for word in mWords:
                if word[0].lower() != word[0]:
                    mWordUpper.append(True)
                else:
                    mWordUpper.append(False)
            text = text.lower()
            if bToRus:
                for key in ccltkr:
                    text = text.replace(key, ccltkr[key])
                for key in cltkr:
                    text = text.replace(key, cltkr[key])
                for key in ltkr:
                    text = text.replace(key, ltkr[key])
            else:
                for key in krlt:
                    text = text.replace(key, krlt[key])
            mWords = String.GetWords(text)
            i = 0
            for word in mWords:
                if mWordUpper[i]:
                    s = word[0].upper() + word[1:]
                    text = text.replace(word, s, 1)
                i += 1
            return text
        except Exception as e:
            Fixer.errlog('StrMorph.Transit', str(e))
            return text
    
