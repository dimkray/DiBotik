import Fixer
from Profiler import Profiler
from Services.Fun import Fun

# автотесты #

with Profiler() as p:
    stest = Fun.Anecdote()
print('Fun.Anecdote:\n[%s]' % stest)

with Profiler() as p:
    stest = Fun.FindAnecdote('%хрен%')
print('Fun.FindAnecdote:\n[%s]' % stest)

##with Profiler() as p:
##    s = '''— Теперь у меня — безлимит!
##        — Поздравляю!
##        — Сломался счетчик воды. Пришел сантехник и снял его на неделю, в ремонт.
##        — Скачаешь мне два ведра горячей воды, пока халява?'''
##    stest = Fun.AddAnecdote(s, 1)
##print('Fun.AddAnecdote:\n[%s]' % stest)

import time; time.sleep(5)
