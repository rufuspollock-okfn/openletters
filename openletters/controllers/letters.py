import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters.transform import transformXml

log = logging.getLogger(__name__)

class LettersController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/letters.mako')
        # or, return a response
        #return 'Hello World'
        #we'll render this at some point 
        author = "Dickens"
        authorIndex = transformXml.createIndex(author)
        return authorIndex
