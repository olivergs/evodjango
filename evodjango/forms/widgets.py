# -*- coding: utf-8 -*-
"""
EVODjango forms
===============================================

.. module:: evodjango.forms.widgets
    :platform: Django
    :synopsis: EVODjango form field widgets module
.. moduleauthor:: (C) 2011 Oliver Gutiérrez

TODO: Fix label for attribute in recaptcha
TODO: Solve recaptcha problems with AJAX forms
"""

# Django imports
from django import forms
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.translation import ugettext_lazy as _

#===============================================================================
# reCAPTCHA widget for reCAPTCHA form fields
#===============================================================================
class RECAPTCHAWidget(forms.widgets.Input):
    """
    reCAPTCHA field widget
    """
    def __init__(self,api_server,pubkey,lang='en',theme='red',*args,**kwargs):
        """
        Initialization method
        """
        self.lang=lang
        self.theme=theme
        self.pubkey=pubkey
        self.api_server=api_server
        super(RECAPTCHAWidget,self).__init__(*args,**kwargs)
    
    def render(self, name, value, attrs={}):
        """
        Render method overload
        """
        return mark_safe(u"""
        <script type="text/javascript">var RecaptchaOptions = {theme : '%s',lang: '%s'};</script>
        <script type="text/javascript" src="%s/challenge?k=%s"></script>
        <noscript>
           <iframe src="%s/noscript?k=%s" width="500" height="300"></iframe>
           <br />
           <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
           <input type="hidden" name="recaptcha_response_field" value="manual_challenge">
        </noscript>
        <input id="%s" type="text" name="recaptcha_django_field" value="" style="display: none;">
        """ % (self.theme,self.lang,self.api_server,self.pubkey,self.api_server,self.pubkey,attrs['id']))

    def value_from_datadict(self, data, files, name):
        """
        Obtaining data from form submission
        """
        return (data.get('recaptcha_challenge_field',None),data.get('recaptcha_response_field',None))

#===============================================================================
# Generic collection widget for generic collection admin inlines
#===============================================================================
class GenericCollectionWidget(forms.Widget):
    """
    Widget for Generic collection foreign key field
    """
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name, value=value)
        return mark_safe(u'<input type="hidden" %s />' % flatatt(final_attrs))

#===============================================================================
# Image input widget with thumbnail for showing current value
#===============================================================================
class ImageInputWidget(forms.FileInput):
    """
    A ImageField Widget for that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(ImageInputWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output=''
        if value and hasattr(value, "url"):
            output='<a target="_blank" href="%s"><img src="%s" /></a> ' % (value.url, value.url)
        output+=super(ImageInputWidget, self).render(name, value, attrs)
        return mark_safe(output)

#===============================================================================
# Location widget with both fields for latitude and longitude
#===============================================================================
class LocationWidget(forms.MultiWidget):
    """
    Location widget
    
    TODO: Location picker using Google Maps
    """
    def __init__(self,attrs={}):
        """
        Initialization method
        """
        widgets=[forms.NumberInput,forms.NumberInput]
        attrs.setdefault('step', 'any')
        super(LocationWidget,self).__init__(widgets=widgets,attrs=attrs)

    def decompress(self,value):
        """
        Decompress value
        """
        if value:
            return [value.get('lat',None),value.get('lon',None)]
        return []

    def format_output(self,rendered_widgets):
        """
        Return formatted output            
        """
        return _('Latitude %s Longitude %s') % (rendered_widgets[0],rendered_widgets[1])

class TinyMCEWidget(forms.Textarea):
    """
    TinyMCE HTML editor widget
    """
    class Media:
        """
        Media class
        """
        extend = False
        js = ('//tinymce.cachefly.net/4.0/tinymce.min.js',)

    def __init__(self, attrs=None):
        final_attrs = {'class': 'tinymce'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(TinyMCEWidget, self).__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None):
        output=super(TinyMCEWidget, self).render(name, value, attrs)
        return mark_safe(output + "<script>tinymce.init({selector: '.tinymce', menubar:false, statusbar: false,});</script>")