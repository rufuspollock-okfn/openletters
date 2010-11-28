import logging, genshi, urllib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort
from routes import redirect_to

from openletters.lib.base import BaseController, render
from openletters import model
from openletters.parse import parse_text, parse_date

from openletters.transform.transform_json import json_transform
from openletters.transform.transform_xml import xml_transform
from openletters.transform.transform_rdf import rdf_transform

from openletters.model import dbase


log = logging.getLogger(__name__)

class LettersController(BaseController):

    ''' 
      Search for letters 
    '''
    def index(self):

        c.corres =  model.Session.query(model.Letter.correspondent).distinct().all()
            
        return render('letters/search.html')
    
    ''' 
      Redirect for search form 
    '''
    def search (self):
        
        sender = request.POST['author']
        recip = request.POST['recipient']

        redirect_to(controller = "letters", action="view", author=sender, correspondent=recip)
        
    
    ''' 
    View returns either the index or the letter text in various formats - json, xml or html -
    depending on the accept header
    
    format of url is /<author name>/<correspondent name>/<letter id>
    '''
    def view(self, author=None, correspondent=None, id=None):
        
        format = request.headers.get('accept','')

        #author is the base collection so cannot be empty
        if author is None:
            abort(404)
          
        query_string = model.Session.query(model.Letter).filter(model.Letter.type == author).all()

        
        if correspondent is not None:
            corr = urllib.unquote(correspondent)
            query_string = model.Session.query(model.Letter).filter(model.Letter.type == author).filter(model.Letter.correspondent == corr).all()
        
        if id is not None:
            query_string = model.Session.query(model.Letter).filter(model.Letter.type == author).filter(model.Letter.correspondent == corr).filter(model.Letter.id == id).all()
            
        if query_string is None or query_string == []:
            abort(404)
        
        if format == "application/json":
            
            response.headers['Content-Type'] = 'application/json'
            json = json_transform()
            return json.to_dict(query_string, id)
        
        elif format == "application/xml":
            response.headers['Content-Type'] = 'text/xml'
            xml = xml_transform()
            
            if id is None:
                return xml.index_xml(query_string)
            else:
                return xml.letter_xml(query_string)
       
        elif format == "application/rdf+xml":
            response.headers['Content-Type'] = 'application/rdf+xml; charset=utf-8'
            rdf = rdf_transform()
            return rdf.create_rdf_letter(query_string)
        
        else:
            if id is None:

                for letter in query_string:
                    c.page_title = "Letters written by " + parse_text.author_full(self, letter.type)
                    if correspondent is not None:
                        c.page_title += " to " + letter.correspondent
                        
                    c.letters = query_string                
                return render('letters/index.html')
            else:
                for letter in query_string:
                    c.page_title = "Letter written from " + parse_text.author_full(self, letter.type) + " to " + letter.correspondent
                    c.author = parse_text.author_full(self, letter.type)
                    c.correspondent = letter.correspondent
                    c.letter_date = letter.letter_date
                    c.letter_text = letter.letter_text
                    c.id = letter.id
                    c.type = model.Session.query(model.Source).get(letter.volume)
                    
                return render('letters/view.html')
    '''
        Method to return a resource view of  the letter
    '''  
    def resource (self, author=None, correspondent=None, id=None, type=None):
        
        #format = request.headers.get('accept','')

        #author is the base collection so cannot be empty
        if author is None:
            abort(404)
          
        query_string = model.Session.query(model.Letter).filter(model.Letter.type == author).all()

        
        if correspondent is not None:
            corr = urllib.unquote(correspondent)
            query_string = model.Session.query(model.Letter).filter(model.Letter.type == author).filter(model.Letter.correspondent == corr).all()
        
        if id is not None:
            query_string = model.Session.query(model.Letter).filter(model.Letter.type == author).filter(model.Letter.correspondent == corr).filter(model.Letter.id == id).all()
            
        if query_string is None or query_string == []:
            abort(404)
        
        if type == "json":
            
            response.headers['Content-Type'] = 'application/json'
            json = json_transform()
            return json.to_dict(query_string, id)
        
        elif type == "xml":
            response.headers['Content-Type'] = 'text/xml'
            xml = xml_transform()
            
            if id is None:
                return xml.index_xml(query_string)
            else:
                return xml.letter_xml(query_string)
       
        elif type == "rdf":
            response.headers['Content-Type'] = 'text/xml'
            rdf = rdf_transform()
            return rdf.create_rdf_letter(query_string)

 

    def corr_dict(self, corr):
        
        letter = {}  
        letter = dbase.get_correspondent(corr)
    
        letter_items = letter.items()
        letter_items.sort()
        
        return letter_items

