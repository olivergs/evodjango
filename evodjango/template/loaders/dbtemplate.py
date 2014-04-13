# -*- coding: utf-8 -*-
###############################################################################
# Author: (C) 2012 Oliver Gutiérrez
# Module: template.loaders.dbtemplate
# Description: EVODjango wrapper for loading templates from a database model
###############################################################################

# Django imports
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.conf import settings

# EVODjango imports
from evodjango.tools import path_import

# Import database template model
try:
	template_model=path_import(settings.DATABASE_TEMPLATES_MODEL)
except ImportError:
	template_model=None

class Loader(BaseLoader):
	is_usable = template_model is not None
	
	def load_template_source(self, template_name, template_dirs=None):
		"""
		Loads templates from a database using an specified model.
		
		Model must have a name and a content fields
		"""
		if template_model is not None:
			try:
				tpl=template_model.objects.get(name=template_name)
				return (tpl.contents,'db:%s' % template_name)
			except:
				pass
		raise TemplateDoesNotExist(template_name)

_loader = Loader()
