import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import urllib

from openletters.lib.base import BaseController, render
from openletters.transform import transform_json, transform_xml, transform_rdf

log = logging.getLogger(__name__)

class DataController(BaseController):
    def json(self, id=None):
        timeline = transform_json.author_timeline(id)
        if id is None:
            abort(404)
        return timeline
    
    def letter_rdf(self, id=None):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        letter_rdf = transform_rdf.create_rdf_letter(id)
        if id is None:
            abort(404)
            
        return letter_rdf
    
    def endpoint(self):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        letter_rdf = transform_rdf.create_rdf_end()
        return letter_rdf
    
    def correspondent(self, id=None):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        corr_rdf = transform_rdf.create_correspondent(id)
        if id is None:
            abort(404)
            
        return corr_rdf
