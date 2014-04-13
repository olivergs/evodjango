# -*- coding: utf-8 -*-
"""
EVODango fields administration module
===============================================

.. module:: evodjango.admin.filters
    :platform: Unix, Windows
    :synopsis: 
    :deprecated:
.. moduleauthor:: (C) 2013 Oliver Gutiérrez
"""
# Python imports
import datetime

# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.filters import FieldListFilter
from django.utils import timezone

class EnhancedDateFieldListFilter(FieldListFilter):
    """
    Modified original django date filter to allow future dates
    """
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_generic = '%s__' % field_path
        self.date_params = dict([(k, v) for k, v in params.items()
                                 if k.startswith(self.field_generic)])

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(field, models.DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:       # field is a models.DateField
            today = now.date()
        tomorrow = today + datetime.timedelta(days=1)

        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_until = '%s__lt' % field_path
        
        # Calculate months
        onemonthlater=today.month+1
        if onemonthlater > 12:
            onemonthlater=1
        twomonthslater=onemonthlater+1
        if twomonthslater > 12:
            twomonthslater =1
        
        self.links = (
            (_('Any date'), {}),
            (_('This year'), {
                self.lookup_kwarg_since: str(today.replace(month=1, day=1)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('This month'), {
                self.lookup_kwarg_since: str(today.replace(day=1)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Past 30 days'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=30)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Past 15 days'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=15)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Past 7 days'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=7)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Yesterday'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=1)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Today'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Tomorrow'), {
                self.lookup_kwarg_since: str(tomorrow),
                self.lookup_kwarg_until: str(tomorrow + datetime.timedelta(days=1)),
            }),
            (_('Next 7 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=7)),
            }),
            (_('Next 15 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=15)),
            }),
            (_('Next 30 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=30)),
            }),
            (_('Next month'), {
                self.lookup_kwarg_since: str(today.replace(day=1,month=onemonthlater)),
                self.lookup_kwarg_until: str(today.replace(day=1,month=twomonthslater)),
            }),
            (_('Next year'), {
                self.lookup_kwarg_since: str(today.replace(day=1,month=1,year=today.year+1)),
                self.lookup_kwarg_until: str(today.replace(day=1,month=1,year=today.year+2)),
            }),
        )
        super(EnhancedDateFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_until]

    def choices(self, cl):
        for title, param_dict in self.links:
            yield {
                'selected': self.date_params == param_dict,
                'query_string': cl.get_query_string(
                                    param_dict, [self.field_generic]),
                'display': title,
            }

FieldListFilter.register(
    lambda f: isinstance(f, models.DateField), EnhancedDateFieldListFilter,take_priority=True)