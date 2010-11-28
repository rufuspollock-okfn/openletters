import logging, urllib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

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
        print "locations", c.places

        return render('letters/magazineindex.html')
    
    def view (self,author=None):
        if author is None:
            abort(404)
        else:
            place = urllib.unquote(author)
            if place == "Gads Hill":
                c.start = '51.2440'
                c.end = '0.2728'
                c.coordinates = '51.2440N 0.2728E'
                c.author = place
                c.abstract = "Gads Hill Place in Higham, Kent, sometimes spelt Gadshill Place and Gad's Hill Place, was the country home of Charles Dickens, the most successful British author of the Victorian era."
                c.mag_url = "http://en.wikipedia.org/wiki/Gads_Hill_Place"
            elif place == 'Tavistock House':
                c.start = '51.5255'
                c.end = '0.1286'
                c.coordinates = '51.5255N  0.1286W'
                c.author = place
                c.abstract = "Tavistock House was the London home of the noted British author Charles Dickens and his family from 1851 to 1860. At Tavistock House Dickens wrote Bleak House, Hard Times, Little Dorrit and A Tale of Two Cities. He also put on amateur theatricals there which are described in John Forster's Life of Charles Dickens. Later, it was the home of William and Georgina Weldon, whose lodger was the French composer Charles Gounod, who composed part of his opera Polyeucte at the house."
                c.mag_url = "http://en.wikipedia.org/wiki/Tavistock_House"
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
            
        print """/
            var markers = new OpenLayers.Layer.Markers( "Markers" );
            map.addLayer(markers);
            
            var size = new OpenLayers.Size(21,25);
            var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
            var icon = new OpenLayers.Icon('http://www.openlayers.org/dev/img/marker.png', size, offset);
            markers.addMarker(new OpenLayers.Marker(new OpenLayers.LonLat(0,0),icon));
        """