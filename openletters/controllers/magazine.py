import logging, urllib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters.transform.transform_json import json_transform
from openletters.transform.transform_xml import xml_transform
from openletters.transform.transform_rdf import rdf_transform

log = logging.getLogger(__name__)

class MagazineController(BaseController):

    def index(self):
        c.magazines = {}
        c.magazines = ["Household Works", "All the Year Round"]
        return render('letters/magazineindex.html')
    
    '''
       Action to return magazine details in html. resource controller = linked data
       Todo: SPARQL query against dbpedia
    '''
    def view (self, author=None):
        
        if author is None:
            c.magazines = {}
            c.magazines = ["Household Works", "All the Year Round"]
            return render('letters/magazineindex.html')
        else:
            mag = urllib.unquote(author)
            if mag =="Household Words":
                c.start = u"March 1850"
                c.end = u"May 1859"
                c.abstract = u"Household Words was an English weekly magazine edited by Charles Dickens in the 1850s which took its name from the line from Shakespeare 'Familiar in his mouth as household words' - Henry V"
                c.mag_url = u"http://en.wikipedia.org/wiki/Household_Words"
            elif mag =="All the Year Round":
                c.start = u"28 January 1859"
                c.end = u"30 March 1895"
                c.abstract = u"All the Year Round was a Victorian periodical, being a British weekly literary magazine founded and owned by Charles Dickens, published between 1859 and 1895 throughout the United Kingdom. Edited by Dickens, it was the direct successor to his previous publication Household Words, abandoned due to differences with his former publisher. It hosted the serialization of many prominent novels, including Dickens' own A Tale of Two Cities. After Dickens's death in 1870, it was owned and edited by his eldest son Charles Dickens, Jr." 
                c.mag_url = u"http://en.wikipedia.org/wiki/All_the_Year_Round"
            else:
                redirect_to(controller='magazine', action='view')
                
            return render('letters/magazine.html')
     

    def resource(self, author=None, correspondent=None):
         '''
           Method to return a resource view of the publication
           @param author publication name
           @param correspondent data type - rdf, json or xml
         '''
         if author is None:
             abort(404)
         else:
             title = str(urllib.unquote(author))
             if correspondent == "rdf":

                 response.headers['Content-Type'] = 'application/rdf+xml;'
                 rdf = rdf_transform()
                 return rdf.create_publication(author, "magazine")
             
             elif correspondent == "json":
                 #response.headers['Content-Type'] = 'application/json'
                 #response.headers['Content-Type'] = 'application/rdf+xml; charset=utf-8'
                 json = json_transform()
                 return json.book_json(author, "magazine")
             
                          
             elif correspondent == "xml":
                 #response.headers['Content-Type'] = 'application/json'
                 #response.headers['Content-Type'] = 'application/rdf+xml; charset=utf-8'
                 json = json_transform()
                 return json.book_json(author, "magazine")
            