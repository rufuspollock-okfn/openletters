import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import urllib

from openletters.lib.base import BaseController, render

from openletters import model

from openletters.transform.transform_rdf import rdf_transform
from openletters.transform.transform_json import json_transform
from openletters.transform.transform_xml import xml_transform

log = logging.getLogger(__name__)

class DataController(BaseController):
    '''
       Return an endpoint in which ever format is requested
    '''
    def endpoint (self, author = '', correspondent = ''):
        
        if author == "rdf":
            response.headers['Content-Type'] = 'text/rdf+xml; charset=utf-8'
            rdf = rdf_transform()
            return rdf.create_rdf_end()
        
        elif author == "json":
            response.headers['Content-Type'] = 'application/json'
            json = json_transform()
            return json.to_end_dict()
        
        elif author == "xml":
            xml = xml_transform()
            response.headers['Content-Type'] = 'text/xml'
            if correspondent == "simile":
                return xml.endpoint_xml("simile")
            else:
                return xml.endpoint_xml()

    def book (self):
        #response.headers['Content-Type'] = 'application/json'
        json = json_transform()
        query_string = model.Session.query(model.Letter).filter(model.Letter.type == author).all()
        return json.book_json(query_string)
    
    def correspondent(self):
        req = request.POST('search')
        corres =  model.Session.query(model.Letter.correspondent).distinct().all()
        
        for c in corres:
            if req in c:
                b = '<li>%s</li>' % c
        
        return b    
    
        