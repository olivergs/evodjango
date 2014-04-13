# -*- coding: utf-8 -*-
"""
EVODjango administration actions module
===============================================

.. module:: evodjango.admin.actions
    :platform: Django
    :synopsis: EVODjango administration actions module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

def clone_register(modeadmin,request,queryset):
    """
    Clone selected registers
    
    Objects get clonated with basic field data.
    Cleaning actions for cloned object will be executed if it has a clone_clean method.
    Extra clone actions will be executed calling clone_extra method for the object
    """
    for obj in queryset:
        # Retrieve a copy of current object
        old=obj.__class__.objects.get(pk=obj.pk)
        # Prepare object for clonation
        obj.pk = None
        obj.id = None
        # Cleaning clone actions
        if hasattr(obj,'clone_clean'):
            obj.clone_clean(request,queryset)
        # Save object and clone it
        obj.save()
        # Execute extra clone actions
        if hasattr(obj,'clone_extra'):
            obj.clone_extra(old)

clone_register.short_description = _('Clone selected registers')

