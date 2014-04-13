# -*- coding: utf-8 -*-
"""
EVODjango form fields
===============================================

.. module:: evodjango.forms.fields
    :platform: Django
    :synopsis: EVODjango form fields module
.. moduleauthor:: (C) 2011 Oliver Gutiérrez
"""

# Python imports
import urllib2, urllib

# Django imports
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from pyevo.checksum import mod10

# EVODjango imports
from evodjango.forms.widgets import RECAPTCHAWidget,LocationWidget,TinyMCEWidget

class EULAField(forms.Field):
    """
    EULA agreement form field class
    """
    def __init__(self,eula_url=None,*args,**kwargs):
        """
        Class initialization
        """
        label=kwargs.get('label',_('I accept the <a href="%s" target="_blank">terms and conditions</a>') % eula_url)
        kwargs['label']=mark_safe(label)
        kwargs.setdefault('widget',forms.CheckboxInput())
        super(EULAField,self).__init__(*args,**kwargs)

    def clean(self,value):
        """
        Check if user has accepted the EULA
        """
        if not value:
            raise forms.ValidationError(_('You have to accept the terms and conditions to continue'))

class RECAPTCHAField(forms.Field):
    """
    reCATCHA form field class
    """
    def __init__(self,pubkey,privkey,
                 api_server='https://www.google.com/recaptcha/api',
                 verify_server='http://www.google.com/recaptcha/api/verify',
                 *args,**kwargs):
        """
        Class initialization
        """
        self.pubkey=pubkey
        self.privkey=privkey
        self.api_server=api_server
        self.verify_server=verify_server
        kwargs.setdefault('widget',RECAPTCHAWidget(self.api_server,self.pubkey))
        super(RECAPTCHAField,self).__init__(*args,**kwargs)

    def clean(self,value):
        """
        reCAPTCHA Validation
        """
        challenge=value[0]
        captcharesp=value[1]
        # Check captcha input
        if not (captcharesp and challenge and len(captcharesp) and len(challenge)):
            raise forms.ValidationError(_('Invalid verification'))
        # Generate request to recaptcha servers
        verifreq = urllib2.Request (
            url = self.verify_server,
            data = urllib.urlencode ({
                'privatekey': self.privkey,
                'remoteip' :  None,
                'challenge':  challenge.encode('utf-8'),
                'response' :  captcharesp.encode('utf-8'),
            }),
            headers = {
                'Content-type': 'application/x-www-form-urlencoded',
                'User-agent': 'Python'
                }
            )
        # Do request
        try:
            resp=urllib2.urlopen(verifreq)
        except:
            # In case of connection error just accept captcha as valid
            return
        # Check captcha response
        return_values=resp.read().splitlines();
        resp.close();
        return_code=return_values[0]
        if (return_code!="true"):
            raise forms.ValidationError(_('Invalid verification'))

class CreditCardField(forms.CharField):
    """
    Credit card form field
    """
    # TODO: Expiration date, CCV, CardType values in credit card form field
    def __init__(self,*args,**kwargs):
        """
        Class initialization
        """
        kwargs.setdefault('max_length', 16)
        super(CreditCardField,self).__init__(*args,**kwargs)

    def clean(self,value):
        """
        Check if credit card number is valid
        """
        if not mod10(value):
            raise forms.ValidationError(_('Invalid credit card number'))

class LocationField(forms.MultiValueField):
    """
    Location field
    """
    def __init__(self, *args, **kwargs):
        """
        Class initialization method
        """
        error_messages = {
            'incomplete': _('Must fill both latitude and longitude'),
        }
        fields=[forms.FloatField(),forms.FloatField()]
        for field in fields:
            field.error_messages={}
        kwargs['widget']=LocationWidget
        super(LocationField, self).__init__(error_messages=error_messages,fields=fields, *args, **kwargs)

    def compress(self,data_list):
        """
        Data compression method
        """
        return dict(zip(('lat','lon'),data_list))

    def clean(self,value):
        """
        Cleaning method
        """
        if value[0] and not value[1] or not value[0] and value[1]:
            raise forms.ValidationError(self.error_messages['incomplete'])
        return super(LocationField,self).clean(value)
