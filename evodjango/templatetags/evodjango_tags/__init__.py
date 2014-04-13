# -*- coding: utf-8 -*-
"""
EVODjango template tags template tags module
===============================================

.. module:: evodjango.templatetags.evodjango
    :platform: Django
    :synopsis: EVODjango template tags module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Django imports
from django import template

# EVODjango imports
from filters import shuffle_list,currency_formatter,file_size_formatter,set_arg,call_method,get_range,html_decode,without_lang,b64encode
from tags.stringrender import stringrender_tag

# Initialize template tag library
register = template.Library()

# Register filters
register.filter('range',get_range)
register.filter('shuffle',shuffle_list)
register.filter('currency',currency_formatter)
register.filter('filesize',file_size_formatter)
register.filter('setarg', set_arg)
register.filter('callmethod', call_method)
register.filter('html_decode', html_decode)
register.filter('without_lang',without_lang)
register.filter('b64encode',b64encode)

# Register tags
register.tag('stringrender',stringrender_tag)
