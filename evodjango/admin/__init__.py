# -*- coding: utf-8 -*-
"""
EVODjango administration module
===============================================

.. module:: evodjango.admin
    :platform: Django
    :synopsis: EVODjango administration module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Django imports
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.utils import flatten_fieldsets

# EVODjango imports
from evodjango.forms.widgets import GenericCollectionWidget

class BaseModelAdminLogic(object):
    """
    Common logic for ModelAdmin classes
    """
    # Extra properties
    all_fields_readonly=False
    superuser_skips_all_readonly=True
    
    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read-only
        """
        if not self.all_fields_readonly or (request.user.is_superuser and self.superuser_skips_all_readonly):
            return self.readonly_fields
        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

class BaseModelAdmin(BaseModelAdminLogic,admin.ModelAdmin):
    """
    Base ModelAdmin administration class
    """
    save_on_top = True
    list_per_page = 50

class BaseTabularInline(BaseModelAdminLogic,admin.TabularInline):
    """
    Base TabularInline administration class
    """
    extra = 0

class BaseGenericTabularInline(BaseModelAdminLogic,GenericTabularInline):
    """
    Base Generic TabularInline administration class
    """
    extra = 0

class TranslatableModelAdmin(BaseModelAdmin):
    """
    Base Translatable ModelAdmin administration class
    """
    # Form fieldsets
    fieldsets_normal=None
    fieldsets_localized=None

    def add_view(self,req,form_url='',extra_context={}):
        """
        Add view method override
        """
        if self.fieldsets_normal:
            self.fieldsets=self.fieldsets_normal
        return super(TranslatableModelAdmin, self).add_view(req,form_url)

    def change_view(self,req,object_id,extra_context={}):
        """
        Change view method override
        """  
        model=self.model.objects.get(id=object_id)

        if model.parent_translation!=None:
            if self.fieldsets_localized:
                self.fieldsets=self.fieldsets_localized
        else:
            if self.fieldsets_normal:
                self.fieldsets=self.fieldsets_normal
        return super(TranslatableModelAdmin, self).change_view(req,object_id)

class GenericCollectionInlineModelAdmin(admin.options.InlineModelAdmin):
    """
    Inline model admin for editing generic relations transparently
    """
    # Generic relation fields
    selector_url=None
    ct_field='content_type'
    ct_fk_field='object_id'
    field_choices={}
    
    def __init__(self,parent_model,admin_site):
        """
        Class initialization
        """
        # Call parent initialization method
        super(GenericCollectionInlineModelAdmin, self).__init__(parent_model, admin_site)
        # Filter for only needed content types
        ct_ids=[]
        for field in self.model._meta.fields:
            if field.name==self.ct_field:
                for choice in field.get_choices():
                    if choice[0]:
                        ct_ids.append(int(choice[0]))
                break
        # Obtain content types list
        ctypes = ContentType.objects.filter(id__in=ct_ids).order_by('id').values_list('id', 'app_label','model')
        # Create javascript map for retrieved content types and save it to seld.content_types
        elements = ["%s: '%s/%s'" % (id, app_label, model) for id, app_label, model in ctypes]
        self.content_types = "{%s}" % ",".join(elements)
    
    def get_formset(self, request, obj=None, **kwargs):
        """
        Get formset method override
        """
        # Call parent initialization method
        result = super(GenericCollectionInlineModelAdmin, self).get_formset(request, obj)
        # Assign content types and values to fields in the formset
        result.content_types = self.content_types
        result.selector_url = self.selector_url
        result.ct_fk_field = self.ct_fk_field
        result.ct_field = self.ct_field
        return result

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Form field for database field method override
        """
        # Call parent initialization method
        field = super(GenericCollectionInlineModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if self.field_choices.has_key(db_field.name):
            field.choices=self.field_choices[db_field.name][0](*self.field_choices[db_field.name][1:])
        # If field is the foreign key to the generic relation change the widget
        if db_field.name == self.ct_fk_field:
            field.widget=GenericCollectionWidget()
        return field

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Form field for foreign key field method override
        """
        field=super(GenericCollectionInlineModelAdmin,self).formfield_for_foreignkey(db_field, request=None, **kwargs)
        if self.field_choices.has_key(db_field.name):
            field.choices=self.field_choices[db_field.name][0](*self.field_choices[db_field.name][1:])
        if db_field.name==self.ct_field:
            field.widget.is_hidden=True
            if hasattr(self,'content_type_choices'):
                field.choices=self.content_type_choices[0](*self.content_type_choices[1:])
        return field

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        Form field for foreign key field method override
        """
        return self.formfield_for_foreignkey(db_field, request, **kwargs)

class GenericCollectionTabularInline(GenericCollectionInlineModelAdmin):
    """
    Inline generic collection variant for tabular inline
    """
    template = 'admin/generic_collection_edit_inline/tabular_inline.html'
 
class GenericCollectionStackedInline(GenericCollectionInlineModelAdmin):
    """
    Inline generic collection variant for stacked inline
    """
    template = 'admin/generic_collection_edit_inline/stacked_inline.html'
