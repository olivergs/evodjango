# -*- coding: utf-8 -*-
"""
EVODjango template filters
===============================================

.. module:: evodjango.templatetags.filters
    :platform: Django
    :synopsis: EVODjango template filters
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""
# Python imports
import random
import base64

# Django imports
from django import template
from django.conf import settings

# PyEVO imports
from pyevo.strings.formatters import currency_formatter,file_size_formatter
from pyevo.html import html_decode

def shuffle_list(arg):
    """
    Return a shuffled copy of a list
    """
    tmp = arg[:]
    random.shuffle(tmp)
    return tmp

def call_method(obj, methodName):
    """
    Execute a method of an object using previously passed arguments with setarg filter
    """
    method = getattr(obj, methodName)
    if hasattr(obj, '__evodjango_call_arguments'):
        ret = method(*obj.__evodjango_call_arguments)
        del obj.__evodjango_call_arguments
        return ret
    return method()
     
def set_arg(obj, arg):
    """
    Pass an argument 
    """
    if not hasattr(obj, '__evodjango_call_arguments'):
        obj.__evodjango_call_arguments = []
    obj.__evodjango_call_arguments += [arg]
    return obj

def get_range(value):
    """
    Return a range of numbers for given value as python range does
    """
    return range(value)

def without_lang(value):
    """
    Removes language part from given
    """
    for lang,langname in settings.LANGUAGES:
        if value.startswith('/' + lang + '/'):
            value=value[len(lang)+1:]
            break
    return value

def b64encode(value):
    """
    Encode a value in base64
    """
    return base64.b64encode(value)