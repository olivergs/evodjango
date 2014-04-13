# -*- coding: utf-8 -*-
"""
HTTP utilities
==============
EVODjango http utilities module has useful HTTP utilities

.. module:: http
    :platform: Django
    :synopsis: EVODjango http related classes module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports
import mimetypes, os, json

# Django imports
from django.http import HttpResponse,StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper

class JSONResponse(HttpResponse):
    """
    **JSON response class**
    
    *Django HttpResponse with support for JSON response*
    """
    def __init__(self,data,*args,**kwargs):
        """
        Class initialization method

        :param data: Data to be serialized to JSON and sent
        :type data: List or dictionary
        """
        content=json.dumps(data)
        kwargs.setdefault('content_type','text/plain')
        # Call parent initialization
        super(JSONResponse,self).__init__(content,*args,**kwargs)

class CSVResponse(HttpResponse):
    """ 
    **CSV response class**
    
    *Django HttpResponse with support for CSV response*
    """
    def __init__(self,data,download_as='file.csv',separator=',',*args,**kwargs):
        """
        Class initialization method

        :param data: Data to be serialized to CSV and sent
        :type data: List of rows
        :param download_as: Filename that will be used for download
        :type download_as: String
        
        TODO: Use csv library instead of manual CSV
        """
        kwargs.setdefault('content_type','text/csv')
        super(CSVResponse,self).__init__(*args,**kwargs)
        self['Content-Disposition'] = 'attachment; filename=%s' % download_as
        # Write CSV data
        #writer = csv.writer(self)
        for row in data:
            #writer.writerow(row)
            self.write(separator.join([str(x) for x in row]) + '\n')

class StaticServeResponse(HttpResponse):
    """
    **Static serve response class**
    
    *Django HttpResponse for serving static content*
    """
    def __init__(self,filepath,backend='django',download_as=None,extra_headers={},*args,**kwargs):
        """
        Class initialization method

        :param filepath: File path you want to serve
        :type filepath: String
        :param backend: Backend you want to use for serving file contents
        :type backend: String
        :param download_as: Filename that will be used for download
        :type download_as: String
        :param extra_headers: Extra headers that will be used in the response
        :type extra_headers: Dictionary
        :raises: ValueError if an invalid backend is specified
        
        .. note:: Valid options for backend parameter are:
        
            * **django**: Use django HTTResponse for sending the file. This backend uses a file wrapper to send file in 8Kb chunks
            * **mod_xsendfile**: Use Apache mod_xsendfile for serving the static file.
            * **nginx_xaccel**: Use nginx X-Accel-Redirect for serving the static file. You can pass extra parameters using extra_headers. Some useful parms are X-Accel-Limit-Rate, X-Accel-Buffering or X-Accel-Charset
        """
        # Guess file mimetype
        content_type=mimetypes.guess_type(filepath)[0]
        kwargs.setdefault('content_type',content_type)
        if backend=='django':
            wrapper = FileWrapper(file(filepath))
            super(StaticServeResponse,self).__init__(wrapper,*args,**kwargs)
            self['Content-Length'] = os.path.getsize(filepath)
        elif backend=='mod_xsendfile':
            super(StaticServeResponse,self).__init__(*args,**kwargs)
            self['X-Sendfile'] = filepath
        elif backend=='nginx_xaccel':
            super(StaticServeResponse,self).__init__(*args,**kwargs)
            self['X-Accel-Redirect'] = filepath
        else:
            raise Exception('Invalid static serving backend')
        # Setup download headers
        if download_as:
            self['Content-Disposition'] = 'attachment; filename=%s' % download_as
        # Setup custom headers
        for k,v in extra_headers.items():
            self[k] = v


class StreamingServeResponse(StreamingHttpResponse):
    """
    **Streaming serve response class**
    
    *Django StreamingHttpResponse for serving static content*
    """
    def __init__(self,filepath,download_as=None,extra_headers={},*args,**kwargs):
        """
        Class initialization method

        :param filepath: File path you want to serve
        :type filepath: String
        :param download_as: Filename that will be used for download
        :type download_as: String
        :param extra_headers: Extra headers that will be used in the response
        :type extra_headers: Dictionary
        """
        # Guess file mimetype
        content_type=mimetypes.guess_type(filepath)[0]
        kwargs.setdefault('content_type',content_type)
        wrapper = FileWrapper(file(filepath))
        super(StreamingServeResponse,self).__init__(wrapper,*args,**kwargs)
        self['Content-Length'] = os.path.getsize(filepath)
        # Setup download headers
        if download_as:
            self['Content-Disposition'] = 'attachment; filename=%s' % download_as
        # Setup custom headers
        for k,v in extra_headers.items():
            self[k] = v
