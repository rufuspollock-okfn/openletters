import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters.transform import transform_json, transform_xml, transform_rdf

log = logging.getLogger(__name__)

class DataController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/data.mako')
        # or, return a response
        response.headers['content-type'] = 'application/json'
        author =  request.params['author']
        timeline = transformJson.authorTimeline(author)
        return timeline
    
    def xml(self):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        author =  request.params['author']
        #authorIndex = transformHtml.outputAuthorIndex(author)
        authorIndex = transformXml.createIndex(author)
        return authorIndex
        
    def letterxml(self):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        letter_url =  request.params['url']
        letterXml = transformXml.createLetter (letter_url)
        return letterXml
    
    def letterrdf(self):
        #response.headers['content-type'] = 'text/xml; charset=utf-8'
        letter_url =  request.params['url']
        letterRdf = transformRdf.createRdfLetter (letter_url)
        return letterRdf