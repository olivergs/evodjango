# -*- coding: utf-8 -*-
"""
EVODjango Context processors
===============================================

.. module:: evodjango.context_processors
    :platform: Django
    :synopsis: EVODjango context processors
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports
import re

def mobile(req):
    """
    Mobile context processor
    """
    MOBILE_USER_AGENTS=[
        r'.*Android.*',
        r'.*iPhone|iPad|iPod.*',
        r'.*Opera Mini.*',
        r'.*Mobile.*',
    ]
    
    mobile=False
    if 'HTTP_USER_AGENT' in req.META:
        uastring=req.META['HTTP_USER_AGENT']
        for uare in MOBILE_USER_AGENTS:
            if re.match(uare, uastring, re.I):
                mobile=True
                break

    return {
        # Mobile browser
        'mobile': mobile,
    }
