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
    def process_response(self, request, response):
        """
        Response processing
        """
        language = translation.get_language()
        if (response.status_code == 404 and
                not translation.get_language_from_path(request.path_info)
                    and self.is_language_prefix_patterns_used()):
            urlconf = getattr(request, 'urlconf', None)
            language_path = '/%s%s' % (language, request.path_info)
            if settings.APPEND_SLASH and not language_path.endswith('/'):
                language_path = language_path + '/'

            if is_valid_path(language_path, urlconf):
                language_url = "%s://%s/%s%s" % (
                    request.is_secure() and 'https' or 'http',
                    request.get_host(), language, request.get_full_path())
                return HttpResponsePermanentRedirect(language_url)
        translation.deactivate()

        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response
