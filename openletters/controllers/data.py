import logging, urllib

from pylons import request, response, session, tmpl_context as c

from openletters import model
from openletters.lib.base import BaseController, render 
from openletters.transform.transform_rdf import rdf_transform
from openletters.transform.transform_json import json_transform
from openletters.transform.transform_xml import xml_transform

log = logging.getLogger(__name__)

class DataController(BaseController):

    def endpoint (self, author = '', correspondent = ''):
        
        '''
          Return an endpoint in which ever format is requested
        '''
        #o = OFS()
        
        if author == "rdf":
            response.headers['Content-Type'] = 'application/rdf+xml'
            #response.headers['Content-Type'] = 'application/rdf+xml
            #for b in o.list_buckets():
            #    g = o.get_stream(b, "endpoint")
            #    return str(g.read())
            rdf = rdf_transform()
            return rdf.create_rdf_end()
        
        elif author == "json":
            response.headers['Content-Type'] = 'application/json'
            #for b in o.list_buckets():
            #    g = o.get_stream(b, "jsonendpoint")
            #    return str(g.read())
            js = json_transform()
            return js.to_end_dict()
        
        elif author == "xml":
            xml = xml_transform()
            response.headers['Content-Type'] = 'application/xml'
            if correspondent == "simile":
                #for b in o.list_buckets():
                #    g = o.get_stream(b, "simileend", True)
                #    return str(g.read())
                return xml.endpoint_xml('simile')

            else:
                #for b in o.list_buckets():
                #    g = o.get_stream(b, "xmlendpoint", True)
                #    return g.read()
                return xml.endpoint_xml()
        else:
            return render("endpoint/index.html")

    def book (self):
        #response.headers['Content-Type'] = 'application/json'
        json = json_transform()
        query_string = model.Session.query(model.Letter).filter(model.Letter.type == author).all()
        return json.book_json(query_string)
    
    '''
       Method to create correspondent rdf
       '''
    def correspondent(self,author=None, correspondent=None):
        
        if correspondent == "rdf":
            response.headers['Content-Type'] = 'application/rdf+xml'
            rdf = rdf_transform()
            return rdf.create_correspondent(author)
        if correspondent == "xml":
            response.headers['Content-Type'] = 'text/xml'
            xml = xml_transform()
            return xml.corres_xml(author)       
    
        if correspondent == "json":
            response.headers['Content-Type'] = 'application/json'
            json = json_transform()
            return json.corr_json(author)
    
    def corres_graph(self):
        return render("viz/network.html") 
 #   def lemmatise (self, author=None):
 #       word_lem = set()
 #       ret_lem = []
 #       for i in wn.synsets(author):
 #           [word_lem.add(lemma.name) for lemma in i.lemmas]
 #           
 #       ret_lem = list(word_lem)
 #       return ret_lem


        
