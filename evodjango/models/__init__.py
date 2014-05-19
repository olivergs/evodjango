# -*- coding: utf-8 -*-
"""
 models module
===============================================

.. module:: evodjango.models
    :platform: Django
    :synopsis: models module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports

# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone, translation
from django.conf import settings

# Import all fields to models module 
from evodjango.models.fields import *


# Applications imports

#class _UserProfileModelBase(ModelBase):
#    """
#    User profile metaclass
#    """
#    # WARNING: _prepare is not part of the public API and may change
#    def _prepare(cls):
#        super(_UserProfileModelBase, cls)._prepare()
#
#        def add_profile(sender, instance, created, **kwargs):
#            """
#            Callback for post_save event on User model to link a new profile to newly created users
#            """
#            if created:
#                cls.objects.create(user=instance)
#        # Automatically link profile when a new user is created
#        post_save.connect(add_profile, sender=User, weak=False)
#
#class UserProfileModel(models.Model):
#    """
#    User profile model
#    """
#    __metaclass__ = _UserProfileModelBase
#    
#    # User model link
#    user = models.OneToOneField(User, primary_key=True)
#
#    class Meta:
#        abstract = True

# Generic model base class
class GenericModel(models.Model):
    """
    Generic relation model
    """
    class Meta:
        """
        Metadata for this model
        """
        abstract=True
    
    content_type = models.ForeignKey(ContentType,verbose_name=_('Content type'),
        help_text=_('Associated content type'))
    object_id = models.PositiveIntegerField(_('Object ID'),
        help_text=_('Associated object identifier'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')

class GenericNullModel(models.Model):
    """
    Generic relation model
    """
    class Meta:
        """
        Metadata for this model
        """
        abstract=True
    
    content_type = models.ForeignKey(ContentType,verbose_name=_('Content type'),blank=True,null=True,
        help_text=_('Associated content type'))
    object_id = models.PositiveIntegerField(_('Object ID'),blank=True,null=True,
        help_text=_('Associated object identifier'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')

class PublishableModel(models.Model):
    """
    Publishable model
    """
    class Meta:
        """
        Metadata for this model
        """
        abstract=True

    publishable_fieldset=('Publication', {
        'description': _('Publication options'),
        # 'classes': ('collapse',),
        'fields': ('publishable_active','publishable_start','publishable_end'),
    })

    publishable_active=models.BooleanField(_('Active'),default=False,db_index=True,
        help_text=_('Indicates if currently active'))
    publishable_start=models.DateTimeField(_('Start'),blank=True,null=True,db_index=True,
        help_text=_('Start publication date'))
    publishable_end=models.DateTimeField(_('End'),blank=True,null=True,db_index=True,
        help_text=_('End publication date'))
    publishable_publishable=models.BooleanField(_('Publishable'),default=True,editable=False,db_index=True,
        help_text=_('Indicates if publishable (Cached value)'))

    def save(self,*args,**kwargs):
        """
        Save method overload
        """
        # Set publishable status on new saved and modified items
        self.publishable_publishable=True
        super(PublishableModel,self).save(*args,**kwargs)

    def is_publishable(self):
        """
        Specifies if this object is publishable

        An object is publishable if:
            * It is active
            * It is in date and time or does not expire
            
        If an object has an associated object is publishable only if the associated one is publishable too
        """
        # By default an object is not publishable
        publishable=False
        # Check if we have an assocciated object and use its data instead self
        assoc=self.get_associated_publishable()
        if assoc:
            return assoc.is_publishable()
        # Check active and not paused
        if self.publishable_active:
            # Check dates
            date=timezone.now()
            if self.publishable_start and date >= self.publishable_start and self.publishable_end and date <= self.publishable_end:
                # Check custom conditions
                publishable=self.extra_check_publishable()
        # Update publishable cached field
        if self.publishable_publishable != publishable:
            self.publishable_publishable=publishable
            self.save()
        return publishable

    def get_associated_publishable(self):
        """
        Returns associated publishable if any
        """
        return None

    def extra_check_publishable(self):
        """
        Extra checks for object publishability
        """
        return True

class TranslatableModel(models.Model):
    """
    Translatable model
    
    TODO: __getattribute__ overload for getting the corresponding translated field information
    """
    class Meta:
        """
        Metadata for this model
        """
        abstract=True

    translatable_fieldset=('Translation', {
        'description': _('Translation data'),
        'fields': ('translatable_lang',),
    })

    translatable_lang=models.CharField(_('Language'),max_length=50,choices=settings.LANGUAGES,db_index=True,
        help_text=_('Language for this model'))
    translatable_parent=models.ForeignKey('self',verbose_name=_('Translated parent'),editable=False,blank=True,null=True,db_index=True,
        help_text=_('Parent item that is translated by this one'))
    
    #def __getattribute__(self, name):
    #    """
    #    Get attribute implementation
    #    """
        # Check attribute existence
        # Get current language
        # Get corresponding language
    
    def save(self,*args,**kwargs):
        """
        Save method overload
        """
        if not self.translatable_lang:
            self.lang=translation.get_language()
        super(TranslatableModel,self).save(*args,**kwargs)
    
    def get_root_translation(self):
        """
        Get root translated model
        """
        if not self.translatable_parent:
            return self
        return self.translatable_parent
    
    def get_translation(self,lang=None):
        """
        Get translation for given language
        """
        # If lang is not specified, we use the current thread language
        if not lang:
            lang=translation.get_language()
        # Get root translation
        parent=self.get_root_translation()
        try:
            return TranslatableModel.objects.get(translatable_parent=parent,translatable_lang=lang)
        except:
            return parent

class UndeletableModel(models.Model):
    """
    Undeletable model
    """
    class Meta:
        """
        Metadata for this model
        """
        abstract=True

    undeletable_deleted=models.BooleanField(_('Deleted'),default=False,editable=False,db_index=True,
        help_text=_('Indicates if this object has been deleted'))

class TimestampedModel(models.Model):
    """
    Timestamped model
    """
    class Meta:
        """
        Metadata for this model
        """
        abstract=True

    timestamped_created=models.DateTimeField(_('Created'),auto_now_add=True,editable=False,db_index=True,
        help_text=_('Creation date and time'))
    timestamped_modified=models.DateTimeField(_('Modified'),auto_now=True,editable=False,db_index=True,
        help_text=_('Modification date and time'))