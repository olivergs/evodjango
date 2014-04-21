# -*- coding: utf-8 -*-
"""
EVODjango utils module
===============================================

.. module:: evodjango.utils
    :platform: Django
    :synopsis: EVODjango utility functions module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports
import sys, os, datetime

# Django imports
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _
from django.core.mail import mail_admins, send_mail
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings

# EVODjango imports
from evodjango.http import StaticServeResponse,StreamingServeResponse

def inject_app_defaults(appname):
    """
    Inject an application's default settings
    """
    try:
        # Import application settings module
        __import__('%s.settings' % appname)
        # Import our defaults, project defaults, and project settings
        _app_settings = sys.modules['%s.settings' % appname]
        _def_settings = sys.modules['django.conf.global_settings']
        _settings = sys.modules['django.conf'].settings
        # Add the values from the application settings module
        for _k in dir(_app_settings):
            if _k.isupper():
                # Add the value to the default settings module
                setattr(_def_settings, _k, getattr(_app_settings, _k))
                
                # Add the value to the settings, if not already present
                if not hasattr(_settings, _k):
                    setattr(_settings, _k, getattr(_app_settings, _k))
    except ImportError:
        # Silently skip failing settings modules
        pass

def get_public_ip(req):
    """
    Get public IP address from a request
    """
    # Public IP discovering
    if 'HTTP_X_FORWARDED_FOR' in req.META:
        pub_ip=req.META['HTTP_X_FORWARDED_FOR']
    else:
        pub_ip=req.META['REMOTE_ADDR']
    return pub_ip

def logged_in_users():
    """
    TODO: Include this method into a manager for users model
    """
    # Query all non-expired sessions
    sessions = Session.objects.filter(expire_date__gte=datetime.datetime.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return get_user_model().objects.filter(id__in=uid_list)

def flatten_response_content(response):
    """
    Flattens a response contents
    """
    # Get content from response
    content=''
    if response.streaming:
        for chunk in response.streaming_content:
            content+=chunk
    else:
        content=response.content
    return content

def static_serve(filepath,backend='django',download_as=None,extra_headers={},*args,**kwargs):
    """
    Static serve tool function
    """
    if os.path.exists(filepath) and not os.path.isdir(filepath):
        if backend=='django':
            # Use StreamingServeResponse
            return StreamingServeResponse(filepath,download_as,extra_headers,*args,**kwargs)
        else:
            # Use StaticServeResponse
            return StaticServeResponse(filepath,backend,download_as,extra_headers,*args,**kwargs)
    else:
        raise Http404(unicode(_('Requested file "%s" does not exist') % filepath))

def send_mail_from_template(recipient_list,subject_template_name,email_template_name,
                            from_email=settings.DEFAULT_FROM_EMAIL,request=None,context={},
                            fail_silently=False,auth_user=None, auth_password=None, connection=None,html=False):
    """
    Send email rendering a template
    """
    if request:
        context.update(RequestContext(request))
    subject=render_to_string(subject_template_name, context)
    subject=''.join(subject.splitlines())
    message=render_to_string(email_template_name, context)
    send_mail(subject, message, from_email, recipient_list, fail_silently, auth_user, auth_password, connection)

def send_mail_to_admins(subject_template_name,email_template_name,request=None,context={},fail_silently=True):
    """
    Send email to administrators
    """
    if request:
        context.update(RequestContext(request))
    subject=render_to_string(subject_template_name, context)
    subject=''.join(subject.splitlines())
    message=render_to_string(email_template_name, context)
    mail_admins(subject, message, fail_silently=True)