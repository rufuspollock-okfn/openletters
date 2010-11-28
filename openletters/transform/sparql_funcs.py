import rdflib,urllib

try:
    from sets import Set
except ImportError:
    from set import Set

try:
    from rdflib.Graph import ConjunctiveGraph as Graph
except ImportError:
    from rdflib.graph import ConjunctiveGraph as Graph

        
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib import Namespace, Literal, URIRef, RDF, RDFS, plugin


''' 
    Functions to use parse the RDF endpoint to build indexes from the RDF data
'''

geo = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
dublin_core = Namespace('http://purl.org/dc/elements/1.1/')

class sparql_funcs():
    
    def __init__(self):
        self.g = Graph('IOMemory')
        self.endpoint = "http://localhost:5000/data/endpoint/rdf"
        #self.g.bind('geo', geo)

    def find_places(self):
        '''
            Function to get the distinct locations mentioned in the headers of the letters. 
            These are the locations from which Dickens wrote. 
            TODO: Parsing the letters to get the places mentioned in them
        '''
        row = set()
        self.g.parse(self.endpoint)

        for s,_,n in self.g.triples((None, dublin_core['title'], None)):
            print "sub", s
            loc_key = urllib.unquote(n.replace("http://www.opencorrespondence.org/place/resource/", ""))
            row.add(self.__tidy_location(loc_key))
        print "row", row
        return row
    
    def __tidy_location (self, location):
        '''
           Function to tidy up some of the places where they refer to the same place
           TODO: prob need some language processing to make this scalable
        '''
        ret_location = '';
        if location == 'Office Of "household Words,':
            ret_location = "Household Words"
        elif location== '"household Words" Office':
            ret_location = "Household Words"
        elif location== '"household Words"':
            ret_location = "Household Words"
        elif location== 'H. W. Office':
            ret_location = "Household Words"
        elif location == '"household Words,':
            ret_location = "Household Words"
        elif location == '"all The Year Round" Office':
            ret_location = "All The Year Round"
        elif location == 'Office Of "all The Year Round,':
            ret_location = "All The Year Round"
        elif location == "Gad's Hill Place":
            ret_location = "Gads Hill"
        elif location == "Gad's Hill":
            ret_location = "Gads Hill"
        elif location == "Gad's Hill Place, Higham":
            ret_location = "Gads Hill"
        elif location == "Tavistock House, Tavistock Square":
            ret_location = "Tavistock House"
        elif location == "London, Tavistock House":
            ret_location = "Tavistock House"
        elif location == "Tavistock House, London":
            ret_location = "Tavistock House"
        else:
            if "U.s." in location:
                location = str(location).replace("U.s", "United States")
            ret_location = str(location).replace(".", "")    
            
        return ret_location