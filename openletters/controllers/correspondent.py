import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters.transform.transform_rdf import rdf_transform

from openletters.model import dbase

log = logging.getLogger(__name__)

class CorrespondentController(BaseController):

    def index(self):
        c.page_title = urllib.unquote(author)
        c.author = author
        c.nicks = self.corr_dict(author)
        
        return render('letters/correspondent.html')
    
    '''
      Method to return details about a correspondent
    '''
    def view(self, author=None):
        
        c.page_title = urllib.unquote(author)
        c.author = author
        c.nicks = self.corr_dict(author)
        
        return render('letters/correspondent.html')
    
    '''
      Method to return details about a correspondent
    '''
    def resource(self, author=None, correspondent=None):
        
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