# -*- coding: utf-8 -*-
"""
EVODjango tools module
===============================================

.. module:: evodjango.tools
    :platform: Unix, Windows
    :synopsis: EVODjango tool functions module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports
import sys, os, calendar, string, random
from PIL import Image, ImageEnhance, ImageStat
from datetime import datetime,timedelta,time
import StringIO

# Django imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template import Context, loader, RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.mail import mail_admins, send_mail
from django.template.loader import render_to_string
from django.conf import settings

# EVODjango imports
from evodjango import utils as evodjango_utils

# Temporary references for compatibility
inject_app_defaults=evodjango_utils.inject_app_defaults
get_public_ip=evodjango_utils.get_public_ip
static_serve=evodjango_utils.static_serve

def reduce_opacity(im,opacity):
    """
    Returns an image with reduced opacity
    """
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

#def crop_image_orig(imagefile,rect,size=None,format='JPEG',filename='cropped.jpg'):
#    """
#    Crops an image at given rectangle and returns a InMemoryUploadedFile instance for use in django
#    """
#    # Create a file-like object to write cropped data
#    fd = StringIO.StringIO()
#    # Load image
#    im=Image.open(imagefile)
#    cropped=im.crop(rect)
#    if size:
#        cropped.resize(size)
#    cropped.save(fd,format=format)            
#    # Create django file upload object and return it
#    return InMemoryUploadedFile(fd, None, filename,'image/%s' % format.lower(), fd.len, None)

def crop_image(imagefile,rect,size=None,format='JPEG',filename='cropped.jpg'):
    """
    Crops an image at given rectangle and returns a InMemoryUploadedFile instance for use in django
    """
    # Load image
    im=Image.open(imagefile)
    cropped=im.crop(rect)
    if size:
        cropped=cropped.resize(size)         
    # Create django file upload object and return it
    return image_to_inmemoryuploadedfile(cropped,filename,format=format)

def image_to_inmemoryuploadedfile(image,filename,format='JPEG'):
    """
    Crops an image at given rectangle and returns a InMemoryUploadedFile instance for use in django
    """
    # Create a file-like object to write cropped data
    fd = StringIO.StringIO()
    # Save image to memory buffer image
    image.save(fd,format=format)            
    # Create django file upload object and return it
    return InMemoryUploadedFile(fd, None, filename,'image/%s' % format.lower(), fd.len, None)

def paginate_items(obj_list,elems=25,pagenum=1):
    """
    Paginate items in a given list
    """
    paginator = Paginator(obj_list, elems) # Show elems per page
    try:
        objs = paginator.page(pagenum)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)
    return objs

def render_template(template_list,context={}):
    """
    Get first available template from given list and renders to an string with given context
    
    :param templates: Template path list
    :type templates: List
    :param context: Context used for template rendering
    :type context: Dictionary
    :returns: Rendered template
    :rtype: String
    """
    template = loader.select_template(template_list)
    return template.render(Context(context))

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
    


    