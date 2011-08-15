import rdflib,urllib

from ofs.local import OFS

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
letter_ns = Namespace('http://www.opencorrespondence.org/schema#')

class sparql_funcs():
    
    def __init__(self):
        self.g = Graph('IOMemory')
        #self.endpoint = "http://www.opencorrespondence.org/data/endpoint/rdf"
        #self.g.bind('geo', geo)


    def find_places(self):
        '''
            Function to get the distinct locations mentioned in the headers of the letters. 
            These are the locations from which Dickens wrote. 
            TODO: Parsing the letters to get the places mentioned in them
        '''
        row = set()
        o = OFS()
        
        for b in o.list_buckets():
            endpoint = o.get_stream(b, "endpoint")

        self.g.parse(endpoint)

        for s,_,n in self.g.triples((None, dublin_core['title'], None)):
            loc_key = urllib.unquote(n.replace("http://www.opencorrespondence.org/place/resource/", "").replace("/rdf",""))
            row.add(self.tidy_location(loc_key))

        return row
    
    def tidy_location (self, location):
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
                location = str(location).replace("U.s", "")
            ret_location = str(location).replace(".", "")    
            
        return ret_location
    
    def find_correspondents(self):
        '''
            Function to get the distinct locations mentioned in the headers of the letters. 
            These are the locations from which Dickens wrote. 
            TODO: Parsing the letters to get the places mentioned in them
        '''
        row = set()
        self.g.parse(self.endpoint)

        for s,_,n in self.g.triples((None, letter['correspondent'], None)):
            loc_key = urllib.unquote(n.replace("http://www.opencorrespondence.org/correspondent/resource/", "").replace("/rdf", ""))
            row.add(loc_key)

        return row
    
    def get_abstract (self, resource_id):
        
        self.g.parse('http://dbpedia.org/resource/'.resource_id)
        q = '''
          SELECT *
                WHERE 
                {
                ?x dbpedia:abstract ?abstract .
                FILTER (lang(?abstract) = 'en')
                }
        '''
        for row in self.g.query(q,
                   initNs=dict(dbpedia=Namespace("http://dbpedia.org/ontology/")),
                   initBindings={}):
            return row[1]

    
    def query_dates(self, author):
        '''query to identify individual dates to a correspondent'''
        q = '''
        SELECT ?date
        FROM <http://localhost:5000/data/endpoint/rdf>
        WHERE {
            ?r dc:subject  \'''' + author + '''\' .  
            ?r dc:date  ?date.  
        }
        '''
        dates = []
        for row in self.g.query(q,
                       initNs=dict(letter=Namespace("http://www.opencorrespondence.org/schema#"), dc=Namespace("http://purl.org/dc/elements/1.1/")),
                       initBindings={}):
            
            date = str(row[0]).split('-')
        
            if date[0][1:].isdigit():
                dates.append(date[0])
        print dates
        dic = {}

        for dt in dates:
            dic[dt] = dates.count(dt)
    
        return dic