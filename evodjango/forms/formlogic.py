# -*- coding: utf-8 -*-
###############################################################################
# Author: (C) 2012 Oliver Gutiérrez
# Module: forms.formlogic
# Description: EVODjango forms logic module
###############################################################################

# Python imports
import uuid

# Django imports
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

# EVODjango imports
from evodjango.http import JSONResponse

class EVODjangoFormLogic(object):
    """
    EVODjango base form class
    """ 
    fieldsets=()
    form_name=str(uuid.uuid4())
    form_template='evodjango/form.html'
    form_method='POST'
    form_action='.'
    submit_label=_('Submit')
    reset_label=_('Reset')
    redir_url=None
    # Ajax options
    ajax=False
    ajax_submit='ajaxsubmit'
    ajax_submit_delay=0
    ajax_presubmit=None
    ajax_success=None
    ajax_error=None
    ajax_complete=None

    def _evodjango_init(self,*args,**kwargs):
        """
        Form logic initialization
        """
        # TODO: Use formsets or modelformsets as needed
        self._evodjango_is_modelform=kwargs.get('is_modelform',False)
        data=[]
        fieldlist=[]
        self.__evodjango_formsets=[]
        
        # Fieldsets processing
        for fieldset in self.fieldsets:
            fieldsetdata={
                'id': slugify(unicode(fieldset[0]._proxy____args[0])),
                'name': fieldset[0],
                'desc': fieldset[1].get('description',''),
                'classes': fieldset[1].get('classes',[]),
                'fields': [],
                'formsets': []
            }
            
            # Formsets
            formsets=fieldset[1].get('formsets',[])
            for fs in formsets:
                exclude=[]
                for field in fs[0]._meta.fields:
                    if field.rel and field.rel.to == self.instance.__class__:
                        exclude.append(field.name)
                formsetclass=modelformset_factory(fs[0],extra=fs[1],exclude=exclude)
                # TODO: Set formset queryset to self.instance related data
                formset=formsetclass(post,files,prefix=self.form_name + '_' + fs[0].__name__.lower(),queryset=fs[0].objects.none())
                fieldsetdata['formsets'].append(formset)
                self.__evodjango_formsets.append(formset)
            
            for field in fieldset[1].get('fields',[]):
                fieldsetdata['fields'].append(self[field])
            data.append(fieldsetdata)

            fieldlist.extend(fieldset[1].get('fields',[]))
            
        fieldlist=list(set(fieldlist))

        # Remove fields that are not in fieldsets
        if self.fieldsets:
            for field in self.fields.keys():
                if field not in fieldlist:
                    del(self.fields[field])

        # Save form fieldsets data
        self.__evodjango_fieldsets_data=data

        # Replace needed Django form methods
        self._django_is_valid=self.is_valid
        self.is_valid=self._evodjango_is_valid
        if self._evodjango_is_modelform:
            self._django_save=self.save
            self.save=self._evodjango_save

    def _evodjango_is_valid(self):
        """
        Return overall validation status
        """
        status=True
        for formset in self.__evodjango_formsets:
            for form in formset:
                status = status and form.is_valid()
        return status and self._django_is_valid()

    def _evodjango_save(self,*args,**kwargs):
        """
        Save method override
        """
        self._django_save(*args,**kwargs)
        for fs in self.get_formsets():
            for form in fs:
                for field in form.instance._meta.fields: 
                    if field.rel and field.rel.to == self.instance.__class__:
                        setattr(form.instance,field.name,self.instance)
            fs.save()

    def get_ajax_call(self):
        """
        Return Javascript AJAX call for the submit button of the form
        """
        return '%s(\'%s\',%s,%s,%s,%s,%s); return false;' % (self.ajax_submit,
                                                             self.form_name,
                                                             self.ajax_submit_delay,
                                                             self.ajax_presubmit or 'null',
                                                             self.ajax_success or 'null',
                                                             self.ajax_error or 'null',
                                                             self.ajax_complete or 'null')

    def get_formsets(self):
        """
        Return formsets data
        """
        return self.__evodjango_formsets

    def get_fieldsets(self):
        """
        Return fieldsets data
        """
        return self.__evodjango_fieldsets_data

    def get_ajax_response(self):
        """
        Perform form validation and return ajax data response
        """
        if not self._evodjango_is_valid():
            data={
                'status': False,
                'errors': {}
            }
            # Add form errors
            for field in self.fields:
                if self[field].errors:
                    data['errors'][self[field].auto_id]=self[field].errors

            
            # Add formset errors
            for formset in self.__evodjango_formsets:
                for form in formset:
                    if not form.is_valid():
                        # Add errors
                        for field in form.fields:
                            if form[field].errors:
                                data['errors'][form[field].auto_id]=form[field].errors
        else:
            data={
                'status': True,
                'url': self.redir_url
            }
        return JSONResponse(data)
