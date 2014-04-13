# -*- coding: utf-8 -*-
"""
Filter related classes and utilities
===============================================

.. module:: models.filters
    :platform: Django
    :synopsis: Filter related classes and utilities 
.. moduleauthor:: (C) 2013 Oliver Gutiérrez
"""

class FilterProcessor(object):
    """
    Filter processor class
    """
    def __init__(self,filterspecs):
        """
        Class initialization
        
        Filter specs format:
        
            filterspecs = {
                'shortcut': (processor, [processor,parameters])
            }
        """
        self.filterspecs=filterspecs        

    def process_simple(self, value, fieldname, valuetype=str, blank=False):
        """
        Returns a simple filter with the value using a cast for valuetype. Valuetype can be also any callable
        """
        # Check empty values
        if not blank and (value=='' or value==None):
            return {}

        return {
            fieldname: valuetype(value)
        }

    def process_range(self, value, fieldname, inclusive=True, blank=False):
        """
        Return a filter for a numeric range
        """
        # Check empty values
        if not blank and (value=='' or value==None):
            return {}

        if inclusive:
            gt='__gte'
            lt='__lte'
        else:
            gt='__gt'
            lt='__lt'
        
        # Get lower and higher extremes
        low,high=value.split('-')

        return {
            fieldname + gt: low,
            fieldname + lt: high,
        }

    def process_multiple(self, value, fieldname, separator=',', blank=False):
        """
        Return a filter for multiple values list
        """
        # Check empty values
        if not blank and (value=='' or value==None):
            return {}

        # Get value list
        if isinstance(value,list):
            valuelist=value
        else:
            valuelist=value.split(separator)

        return {
            fieldname + '__in': valuelist
        }

    def process_direct(self, value, filters, checkcallback=None):
        """
        Return a filter for direct rules if value is evaluable as not empty
        """
        # Check empty values
        if not value:
            return {}
        return filters

    def get_filters(self,filterdata,return_clean=False):
        """
        Process filter data and return a filters dictionary
        
        filterdata: dict of shortcut-value items
        """
        # Process filter data using given specs
        filters={}
        cleanfilters={}
        for shortcut,value in filterdata.items():            
            if shortcut in self.filterspecs:
                processor=self.filterspecs[shortcut][0]
                parms=self.filterspecs[shortcut][1]
                if isinstance(processor,str):
                    if processor=='multiple' and '[]' == shortcut[-2:]:
                        value=filterdata.getlist(shortcut)
                        shortcut=shortcut[:-2]
                    processor=getattr(self, 'process_' + processor)
                try:
                    filters.update(processor(value,*parms))
                    cleanfilters[shortcut]=value
                except:
                    pass
        # Return processed filters
        if return_clean:
            return filters,cleanfilters
        return filters

    