# -*- coding: utf-8 -*-
"""
EVODjango forms
===============================================

.. module:: evodjango.forms
    :platform: Django
    :synopsis: EVODjango forms module
.. moduleauthor:: (C) 2011 Oliver Gutiérrez
"""

# Django imports
from django import forms as djangoforms

# EVODjango imports
from formlogic import EVODjangoFormLogic 
from evodjango.forms.fields import *

class EVODjangoForm(djangoforms.Form,EVODjangoFormLogic):
    """
    EVODjango base form class
    """
    def __init__(self,*args,**kwargs):
        """
        Class initialization method
        """
        super(EVODjangoForm, self).__init__(*args,**kwargs)
        super(EVODjangoForm, self)._evodjango_init(*args,**kwargs)

class EVODjangoModelForm(djangoforms.ModelForm,EVODjangoFormLogic):
    """
    EVODjango base modelform class
    """
    def __init__(self,*args,**kwargs):
        """
        Class initialization method
        """
        super(EVODjangoModelForm, self).__init__(*args,**kwargs)
        kwargs.update({'is_modelform':True})
        super(EVODjangoModelForm, self)._evodjango_init(*args,**kwargs)
