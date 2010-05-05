import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters.transform import transform_json, transform_xml, transform_rdf

log = logging.getLogger(__name__)

class DataController(BaseController):

    def index_json(self):
        # Return a rendered template
        #return render('/data.mako')
        # or, return a response
        response.headers['content-type'] = 'application/json'
        author =  request.params['author']
        timeline = transform_json.authorTimeline(author)
        return timeline
    
    def index_xml(self):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        author =  request.params['author']
        #authorIndex = transformHtml.outputAuthorIndex(author)
        authorIndex = transform_xml.createIndex(author)
        return authorIndex
        
    def letter_xml(self):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        letter_url =  request.params['url']
        letterXml = transform_xml.createLetter (letter_url)
        return letterXml
    
    def letter_rdf(self):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        letter_url =  request.params['url']
        letter_rdf = transform_rdf.createRdfLetter (letter_url)
        return letter_rdf
    
    def endpoint(self):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        letter_rdf = transform_rdf.create_rdf_end ()
        return letter_rdf