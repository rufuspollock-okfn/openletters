import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters.transform import transformXml
from openletters.transform import transformHtml

log = logging.getLogger(__name__)

class LettersController(BaseController):
#hardcoded variables to change 
    def index(self):
        author = "Dickens"
        authorIndex = transformHtml.outputAuthorIndex(author)
        return authorIndex
    
    def letter (self):
        #self.uri = uri
        uri = ("3misshogarth")
        letterHtml = transformHtml.outputLetter(uri)
        
        return letterHtml
        
    def xml(self):
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        author = "Dickens"
        #authorIndex = transformHtml.outputAuthorIndex(author)
        authorIndex = transformXml.createIndex(author)
        return authorIndex
        
