import logging, urllib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from ofs.local import OFS

from openletters.lib.base import BaseController, render

from openletters import model

from openletters.transform.transform_json import json_transform
from openletters.transform.transform_xml import xml_transform
from openletters.transform.transform_rdf import rdf_transform

from openletters.transform.sparql_funcs import sparql_funcs

log = logging.getLogger(__name__)

'''
   Controller to show the geographical place. 
   Need a callback to get a lat/long
   Shows html in view
   Show rdf, json and xml in resource
'''

class PlaceController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/place.mako')
        # or, return a response
        sparql = sparql_funcs()
        locations = []
        locations = list(sparql.find_places())
        c.places = sorted(locations)
        #print "locations", c.places

        return render('letters/magazineindex.html')
    
    def view (self,author=None):

        
        if author is None:
            abort(404)
        else:
            
            query_string = model.Session.query(model.Place).filter(model.Place.place == author)

            c.author = locations[urllib.unquote(author)]
            c.start = locations[0]
            c.end = locations[1]
            c.coordinates = str(locations[0]) + ' ' + str(locations[1])
            c.description = locations[2]

            return render('letters/magazine.html')
    
    def resource (self, author=None, correspondent=None):
        if author is None:
            abort(404)
        else:
            place =  str(urllib.unquote(author))
        if correspondent == "rdf":
            response.headers['Content-Type'] = 'text/xml; charset=utf-8'
            rdf = rdf_transform()
            return rdf.create_place(place)
        
    def map (self, author=None):
        response.headers['Content-Type'] = 'text/javascript'
        lat = ''
        long = ''
        place = urllib.unquote(author)
        if place == "Gad's Hill":
            lat = '51.2440'
            long = '0.2728'
        elif place == 'Tavistock House':
            lat = '51.5255N'
            long = '0.1286W'
    
    def getText(nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(unicodedata.normalize('NFKC', node.data))
        return ''.join(rc)

    def handle_elements (elementname, element):
        e = element.getElementsByTagName(elementname)
        
        for name in e:
            return self.handle_parts(elementname, name)
    
        
    def handle_parts (nodename, node):
        return self.getText(node.childNodes)
            
    # there's probably a better way to do this 
    # but the next task is data processing so we can sort then
    
    def place_element(placestr):
        place = ''

        if "Baltimore" in placestr:
            place = "Baltimore"
        if "Bath" in placestr:
            place = "Bath"
           
        if "Birmingham" in placestr:
            place = "Birmingham"
        if "Brighton" in placestr:
            place = "Brighton"
        if "Boulogne" in placestr:
            place = "Boulogne"
        if "Boston" in placestr:
            place = "Boston"
        if "Clifton" in placestr:
            place = "Clifton"
        if "Canterbury" in placestr:
            place = "Canterbury"
        if "Dover" in placestr:
            place = "Dover"
        if "Glasgow" in placestr:
            place = "Glasgow"
        if "Great Malvern" in placestr:
            place = "Great Malvern"
        if "Liverpool" in placestr:
            place = "Liverpool"
        if "Petersham" in placestr:
            place = "Petersham"
        else:
            place = placestr
                                                                    
        return place