# -*- coding: utf-8 -*-
"""
EVODjango model fields
===============================================

.. module:: evodjango.models.fields
    :platform: Django
    :synopsis: EVODjango model fields module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""
# Python imports
import json

# Django imports
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# EVODjango imports
from evodjango import enums
from evodjango.forms import LocationField as LocationFormField, TinyMCEWidget

class GenderField(models.CharField):
    """
    Gender selection field
    """
    description = _('Internationalization CharField')
    __metaclass__ = models.SubfieldBase
    

    def __init__(self, *args, **kwargs):
        """
        Class initialization method
        """
        kwargs.setdefault('max_length', 1)
        kwargs.setdefault('choices', enums.GENDERS)
        super(GenderField, self).__init__(*args, **kwargs)

class CountryField(models.CharField):
    """
    Country selection field
    """
    description = _('Country selection field')
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        """
        Class initialization method
        """
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', enums.COUNTRIES)
        super(CountryField, self).__init__(*args, **kwargs)

class CurrencyField(models.CharField):
    """
    Currency selection field
    """
    description = _('Currency selection field')
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        """
        Class initialization method
        """
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('choices', enums.CURRENCY_CODES)
        super(CurrencyField, self).__init__(*args, **kwargs)

class LanguageField(models.CharField):
    """
    Language selection field
    """
    description = _('Language selection field')
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        """
        Class initialization method
        """
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', settings.LANGUAGES)
        super(LanguageField, self).__init__(*args, **kwargs)

class EncodedField(models.TextField):
    """
    Encoded data field
    """
    description = _('Encoded data field')
    __metaclass__ = models.SubfieldBase
    
    def __init__(self,*args, **kwargs):
        """
        Initialization method
        """
        self.encodecb=kwargs.pop('encoder',None)
        if self.encodecb is None:
            raise ValueError(_('No encoder callback defined'))
        self.decodecb=kwargs.pop('decoder',None)
        if self.decodecb is None:
            raise ValueError(_('No decoder callback defined'))
        super(EncodedField,self).__init__(*args, **kwargs)
    
    def dummy_encode_decode(self,value):
        """
        Dummy enconde/decode method for raising not implemented error
        """

    def to_python(self,value):
        """
        Python object casting method
        """
        return self.decodecb(value)

    def get_prep_value(self,value):
        """
        DB object casting method
        """
        return self.encodecb(value)

class JSONField(EncodedField):
    """
    JSON data field
    """
    description = _('JSON encoded data field')
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        """
        Initialization method
        """
        super(JSONField,self).__init__(encoder=json.dumps,decoder=self.decode_json, *args, **kwargs)
    
    def decode_json(self,value):
        """
        Python object casting method
        """
        if not value:
            return {}
        elif isinstance(value, dict):
            return value
        return json.loads(value)

class LocationField(JSONField):
    """
    Location field class
    """
    description = _('JSON encoded latitude and longitude')
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        """
        Form field method overload
        """
        return super(LocationField,self).formfield(form_class=LocationFormField,**kwargs)

    def contribute_to_class(self, cls, name):
        """
        Contribute to class adding get_FIELD_display method to the model containing this field
        """
        def get_location_display(modelobj,lang=None):
            """
            Function to show localized version of a field
            """
            data=getattr(modelobj,name)
            if data:
                return '(%s,%s)' % (data['lat'],data['lon'])
            return None
        
        # TODO: Set verbose name for field in short description for display method
        #get_location_display.short_description=getattr(cls,name).verbose_name
        #get_location_display.short_description=getattr(cls,name).verbose_name
        #getattr(cls, 'get_%s_display' % name).short_description=getattr(cls,name).short_description

        # Set attribute
        setattr(cls, 'get_%s_display' % name, get_location_display)
        
        # Call original method
        super(LocationField,self).contribute_to_class(cls, name)

class EXIFField(JSONField):
    """
    EXIF data field
    
    TODO: Create special imagefield that can set a exiffield  or get a parameter for image field to be examined for EXIF in this field
    TODO: Add contribution methods to get exif tags values from model
    """
    pass
