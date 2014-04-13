# -*- coding: utf-8 -*-
"""
EVODjango administration widgets module
===============================================

.. module:: evodjango.admin.widgets
    :platform: Django
    :synopsis: EVODjango administration widgets module 
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Django imports
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class AdminImageFileWidget(AdminFileWidget):
    """
    Custom administration system widget for image fields
    """
    def render(self, name, value, attrs=None):
        """
        HTML Rendering
        """
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            output.append('<a target="_blank" href="%s"><img src="%s" height="100"/></a><br /><a target="_blank" href="%s">%s</a><br /> ' % \
                (file_path, file_path, _('Currently:'), _('Change:')))

        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
