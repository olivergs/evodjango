# -*- coding: utf-8 -*-
"""
 views module
===============================================

.. module:: evodjango.views
    :platform: Django
    :synopsis: views module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports
import os

# Django imports
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response
from django.conf import settings

# EVODjango imports
from evodjango.utils import static_serve as evodjango_static_serve

def favicon(req,favicon_path='favicon.ico',backend='django'):
    """
    Favicon serving 
    """
    return evodjango_static_serve(settings.STATIC_ROOT + favicon_path,backend,extra_headers={'Content-Type': 'image/vnd.microsoft.icon'})

def simple_robots(req,options={}):
    """
    Robots view
    """
    try:
        data=render_to_string('robots.txt',options)
    except Exception,e:
        raise Http404('Error loading robots file: %s' % e)
    # Generate advertisement page
    return HttpResponse(data,mimetype='text/plain')

def process_form(req,template,formclass):
    """
    Basic form processing
    """
    if req.method == 'POST':
        # A form bound to the POST data
        form = formclass(req.POST)
        if form.is_valid():
            # Create player
            return form.process_form(req)
    else:
        # An unbound form
        form = formclass()
    ctx={
        'form': form 
    }
    return render_to_response(template,ctx,context_instance=RequestContext(req))

def static_serve(req,path,backend='django'):
    """
    Static serving
    """
    return evodjango_static_serve(settings.STATIC_ROOT + path,backend)

#def media_serve(req,path,check_callback=None):
#    """
#    Media serving
#    
#    TODO: Last-Modified header must be set
#    """
#
#    def last_mod(*args,**kwargs):
#        try:
#            return last_modification_datetime(settings.STATIC_ROOT + kwargs['path'])
#        except:
#            return datetime.datetime.now()
#    
#    def generate_expiration():
#        date = datetime.datetime.now() + datetime.timedelta(days=7)
#        return date.strftime('%a, %d %b %Y %H:%M:%S GMT')
#
#
#
#    photo=None
#    fpath=cache.get('fpath%s' % photoid,None)
#    if fpath is None:
#        photo=get_object_or_404(AdPhoto,id=photoid)
#        fpath=photo.photo.path
#        cache.set('fpath%s' % photoid,fpath,60)
#    if not req.META.has_key('HTTP_REFERER') or not sitere.match(req.META['HTTP_REFERER']):
#        if photo is None:
#            photo=get_object_or_404(AdPhoto,id=photoid)
#        if not photo.active or not photo.ad.is_publishable() and not req.user.is_staff and not photo.ad.owner==req.user:
#            raise Http404(unicode(_('Photo advertisement is not publishable')))
#    if fpath:
#        return evodjango_static_serve(fpath,backend=settings.STATIC_SERVE_BACKEND,extra_headers={'Expires': generate_expiration() })
#    else:
#        raise Http404(unicode(_('Photo not available in specified size')))

