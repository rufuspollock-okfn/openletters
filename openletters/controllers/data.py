import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import urllib

from openletters.lib.base import BaseController, render
from openletters.transform.transform_rdf import rdf_transform

log = logging.getLogger(__name__)

class DataController(BaseController):
    
    def endpoint (self):
        response.headers['Content-Type'] = 'application/rdf+xml; charset=utf-8'
        rdf = rdf_transform()
        
        return rdf.create_rdf_end()
