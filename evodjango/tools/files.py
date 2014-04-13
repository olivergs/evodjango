# -*- coding: utf-8 -*-
"""
EVODjango upload tools
===============================================

.. module:: evodjango.tools.upload
    :platform: Django
    :synopsis: EVODjango upload tools
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports
import os

# Django imports
from django.utils import timezone

class UploadPath(object):
    """
    Filename and path generator
    """
    def __init__(self,prefix='',filename='',datepath=False,timestamped=False,generator=None):
        """
        Initialization method
        """
        self.prefix=prefix
        self.filename=filename
        self.datepath=datepath
        self.timestamped=timestamped
        self.generator=generator
            
    def __call__(self,instance,filename):
        """
        Call method overload for generating upload path
        """
        if self.generator:
            return self.generator(instance,filename)
        else:
            path=self.prefix
            fname,fext=os.path.splitext(filename)
            now=timezone.now()
            
            if self.datepath:
                path+=now.strftime('%Y/%m/%d/')

            if self.filename:
                fname=self.filename
            else:
                if self.timestamped:
                    fname=now.strftime('%s')
            return '%s%s%s' % (path,fname,fext)