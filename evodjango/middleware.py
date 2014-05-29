# -*- coding: utf-8 -*-
"""
EVODjango middleware classes module
===============================================

.. module:: middleware
    :platform: Django
    :synopsis: EVODjango middleware classes module
.. moduleauthor:: (C) 2013 Oliver Gutiérrez
"""

# Django imports
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import is_valid_path
from django.middleware.locale import LocaleMiddleware
from django.shortcuts import redirect
from django.utils import translation
from django.utils.cache import patch_vary_headers
from django.conf import settings

class CaseInsensitiveURLMiddleware(object):
    """
    SEO Friendly locale middleware
    """
    def process_request(self, request):
        """
        Request processing
        """
        try:
            whitelist=settings.CASE_SENSITIVE_PATHS
        except:
            whitelist=[]
        lpath=request.path.lower()
        if request.path != lpath and request.path not in whitelist:
            return redirect(lpath,permanent=True)
        return None

class SEOFriendlyLocaleMiddleware(LocaleMiddleware):
    """
    SEO Friendly locale middleware
    """
    response_redirect_class = HttpResponsePermanentRedirect
