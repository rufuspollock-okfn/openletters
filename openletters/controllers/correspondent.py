import logging, urllib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render
from openletters import model
from openletters.model import dbase

from openletters.parse import parse_text, parse_date

from openletters.transform.transform_json import json_transform
from openletters.transform.transform_xml import xml_transform
from openletters.transform.transform_rdf import rdf_transform

from openletters.transform.sparql_funcs import sparql_funcs

log = logging.getLogger(__name__)

class CorrespondentController(BaseController):

    def index(self):
        c.page_title = "Index of correspondents"

        c.corres =  model.Session.query(model.Letter.correspondent).distinct().all()

        return render('letters/correspondent.html')
    

    def view(self, author=None):
        '''
              Method to return details about a correspondent
        '''
        sparql = sparql_funcs()
        
        c.page_title = urllib.unquote(author)
        c.author = author
        #indexdata = model.Session.query(model.Letter.correspondent).distinct().all()
        query_string = model.Session.query(model.Letter).filter(model.Letter.correspondent == author).all()

        salutation = []
        for letter in query_string:
            salutation.append(letter.salutation)
            c.letters = query_string
            place = parse_text.find_geographical(letter.letter_text)
            if place is not None or place is not "No Place":
                c.placeid = " ".join(letter.letter_place.split("_"))
                c.place = letter.letter_place
                c.type = model.Session.query(model.Source).get(letter.volume)
           
        #letter_items = salutation.items()
        salutation.sort()         
        c.nicks = self.corr_dict(author)
        
# needs call to get date data
        dates = []
        data = sparql.query_dates(author)

        c.dates_data = '['
        for k, v in sorted(data.items()):
            c.dates_data += str(v) + ','
        c.dates_data += ']'
        
        c.xdates = len(data)+1
        return render('letters/correspondent.html')
    

    def resource(self, author=None, correspondent=None):
        
        '''
          Method to return details about a correspondent
        '''
        if author is None:
            abort(404)

        if correspondent == "rdf" or correspondent is None:
            response.headers['content-type'] = 'text/xml; charset=utf-8'
            rdf = rdf_transform()
            return rdf.create_correspondent(author, self.corr_dict(author))
        
        elif correspondent == "xml":
            response.headers['content-type'] = 'text/xml; charset=utf-8'
            xml = xml_transform()
            return xml.corres_xml(author, self.corr_dict(author))
        
        elif correspondent == "json":
            response.headers['content-type'] = 'application/json;'
            json = json_transform()
            return json.corr_json(author, self.corr_dict(author))

    
    def corr_dict(self, corr):
        
        letter = {}  
        letter = dbase.get_correspondent(corr)
    
        letter_items = letter.items()
        letter_items.sort()
        
        return letter_items
    