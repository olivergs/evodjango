# -*- coding: utf-8 -*-
"""
EVODjango model managers module
===============================================

.. module:: evodjango.models.managers
    :platform: Django
    :synopsis: EVODjango model managers module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports

# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class PublishableModelManager(models.Manager):
    """
    Publishable model manager
    """
    def get_publishables(self,**filters):
        """
        Get all posts for a given tag and filters
        """
        # Filter by active publishables
        qs=self.get_queryset().filter(publishable_active=True)
        # Filter by publishable start and end date
        timestamp=timezone.now()
        qs=qs.filter(models.Q(publishable_start=None) | models.Q (publishable_start__lte=timestamp))
        qs=qs.filter(models.Q(publishable_end=None) | models.Q (publishable_end__gte=timestamp))
        return qs.filter(**filters)