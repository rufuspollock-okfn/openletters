import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters import model

from openletters.transform.transform_json import json_transform
from openletters.transform.transform_xml import xml_transform
from openletters.transform.transform_rdf import rdf_transform

log = logging.getLogger(__name__)

class BookController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/book.mako')
        # or, return a response
        c.titles = model.Session.query(model.Book).all()

        return render('letters/magazineindex.html')
    
    def view (self, author=None):
        
        if author is None:
            abort(404)
        
        else:
            c.books = model.Session.query(model.Book).filter(model.Book.url == author)
            return render('letters/book.html')
        
    def resource (self, author=None, correspondent=None):
        
        if author is None:
            abort(404)
            
        if correspondent is None:
            redirect_to(controller="book", action="view", author=author)
        
        else:
            books = model.Session.query(model.Book).filter(model.Book.url == author)
            if correspondent == "rdf":
                #response.headers['Content-Type'] = 'application/rdf+xml'
                rdf = rdf_transform()
                return rdf.create_publication(author, "book")
            if correspondent == "json":
               # response.headers['Content-Type'] = 'application/json'
                json = json_transform()
                return json.book_json(author, "book")