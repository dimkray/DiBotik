# -*- coding: utf-8 -*-
# Сервис по работе с функциями и процедурами
import Fixer
import inspect
from Tests.Testing import Test

def uniq(seq): 
    return list(set(seq))

# Полчение списка всех функций указанного класса (включая системные)
def GetAllMembers(iclass):
    ret = dir(iclass)
    if hasattr(iclass,'__bases__'):
        for base in iclass.__bases__:
            ret = ret + GetAllMembers(base)
    return ret

# Получение всех атрибутов указанного класса/объекта (включая системные)
def GetAllAttrs(obj):
    ret = dir(obj)
    if hasattr(obj,'__class__'):
        ret.append('__class__')
        ret.extend(GetAllMembers(obj.__class__))
        print(ret)
        ret = uniq(ret)
        print(ret)
    return ret

# Получение всех активных глобальных объектов (списком)
def GetGlobals():
    mlist = []
    for key in globals():
        if not key.startswith("__"): mlist.append(key)
    return mlist

# Получение указанного класса
def GetClass(name):
    cl = globals()[name]
    return cl

# Полчение списка всех функций указанного класса
def GetMembers(iclass):
    mlist = []
    for i in GetAllMembers(iclass):
        if not i.startswith("__"):
            mlist.append(i)
    return mlist

# Получение всех атрибутов указанного класса
def GetAttrs(obj):
    mlist = []
    for i in GetAllAttrs(obj):
        if not i.startswith("__"): mlist.append(i)
    return mlist

# Получение всех аргументов указанной функции
def GetArgs(member):
    argspec = inspect.getfullargspec(member)
    return argspec.args

# Запуск кода
def Code(code):
    try:
        return eval(code)
    except Exception as e: 
        Fixer.errlog('Def.Code', str(e))
        return '#bug: ' + str(e)

# Запуск функции из сервиса с аргументами
def Run(module, nameclass, namedef, *args):
    try:
        import importlib, sys
        mod = sys.modules[module]
        if nameclass != '':
            cl = getattr(mod, nameclass)
            func = getattr(cl, namedef)
        else: func = getattr(mod, namedef)
        return func(*args)
    except Exception as e: 
        Fixer.errlog('Def.Run', str(e))
        return '#bug: ' + str(e)
