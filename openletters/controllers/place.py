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
        #sparql = sparql_funcs()
        #locations = []
        #locations = list(sparql.find_places())
        #c.places = sorted(locations)
        #print "locations", c.place
        c.places =  model.Session.query(model.Location.url).distinct().all()

        return render('letters/magazineindex.html')
    
    def view (self,author=None):

        
        if author is None:
            abort(404)
        else:
            c.page_title = "Location for " + author
            query_string = model.Session.query(model.Location).filter(model.Location.url == author)

            for location in query_string:
                c.author = location.placeid
                c.start = location.latitude
                c.end = location.longitude
                c.coordinates = str(location.latitude) + ' ' + str(location.longitude)
                c.description = location.source

            return render('letters/magazine.html')
    
    def resource (self, author=None, correspondent=None):
        if author is None:
            abort(404)
            
        placeobj = model.Session.query(model.Location).filter(model.Location.url == author)

        if correspondent == "rdf":
            response.headers['Content-Type'] = 'text/xml; charset=utf-8'
            rdf = rdf_transform()
            return rdf.create_place(placeobj)
    
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