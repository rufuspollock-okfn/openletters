import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters.transform import transformXml, transformHtml

log = logging.getLogger(__name__)

class LettersController(BaseController):
#hardcoded variables to change 
    def index(self):
        author =  request.params['author']

        authorIndex = transformHtml.outputAuthorIndex(author)
        return authorIndex
    
    def letter (self):
        #self.uri = uri
        uri =  request.params['letter']
        letterHtml = transformHtml.outputLetter(uri)
        
        return letterHtml
        
        
