# -*- coding: utf-8 -*-
"""
EVODjango decorators
===============================================

.. module:: evodjango.decorators
    :platform: Django
    :synopsis: EVODjango decorators module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports
from functools import wraps
import os,time,hotshot

# Django imports
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.utils.decorators import available_attrs

# EVODjango imports
from evodjango.utils import get_public_ip

def ajax_or_redirect(redirect_url='/'):
    """
    Decorator for views that checks that the request is an AJAX request, redirecting
    to the specified URL if it is not.
    
    :param redirect_url: Value to be checked
    :type redirect_url: An absolute or relative URL
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(req, *args, **kwargs):
            if req.is_ajax():
                return view_func(req, *args, **kwargs)
            return HttpResponseRedirect(redirect_url)
        return _wrapped_view
    return decorator

def check_ip(ip_list,errorcode=403,redirect_url=None):
    """
    Decorator to check client IP is allowed returning an error or redirecting to
    the specified URL in case of it is not.

    :param ip_list: List of allowed IP addresses
    :type ip_list: list    
    :param statuscode: Status code for denied requests
    :type statuscode: int
    :param redirect_url: Value to be checked
    :type redirect_url: An absolute or relative URL
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(req, *args, **kwargs):
            ip=get_public_ip(req)
            if ip not in ip_list:
                if redirect_url is not None:
                    return HttpResponseRedirect(redirect_url) 
                else:
                    return HttpResponse(status=errorcode)
            return view_func(req, *args, **kwargs)
        return _wrapped_view
    return decorator

def ajax_or_404(view_func):
    """
    Decorator for views that checks that the request is an AJAX request, showing a
    404 error page if it is not.
    """
    def _wrapped_view(req, *args, **kwargs):
        if req.is_ajax():
            return view_func(req, *args, **kwargs)
        raise Http404
    return _wrapped_view

def performance_profile(log_dir):
    """
    Function profiling decorator
    """
    if not os.path.isabs(log_dir):
        raise ValueError('An absolute path is needed for profile log dir')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    else:
        if not os.path.isdir(log_dir):
            raise ValueError('Specified profile log dir is not a directory')

    def _outer(f):
        def _inner(*args, **kwargs):
            # Generate a file with current time as name
            fname=time.strftime("%Y%m%dT%H%M%S", time.gmtime()) + '.prof'
            final_log_file = os.path.join(log_dir,fname) 
            prof = hotshot.Profile(final_log_file)
            try:
                ret = prof.runcall(f, *args, **kwargs)
            finally:
                prof.close()
            return ret
        return _inner
    return _outer