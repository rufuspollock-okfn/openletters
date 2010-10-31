from openletters.model import dbase
from openletters.parse import parse_text
import urllib, rdflib

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



letter_ns = Namespace('http://purl.org/letter/')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
XSD_NS = Namespace(u'http://www.w3.org/2001/XMLSchema#')
owl_time = Namespace('http://www.isi.edu/~pan/damltime/time-entry.owl#')
dublin_core = Namespace('http://purl.org/dc/elements/1.1/')
base_uri = "http://www.opencorrespondence.org/"

class rdf_transform:
    
    def __init__(self):
        
        self.g = Graph('IOMemory')
        self.g.bind('dc', dublin_core)
        self.g.bind('foaf', FOAF)
        self.g.bind('time-entry', owl_time)
        self.g.bind('letter', letter_ns)
        self.g.bind('base', base_uri)

    '''
      creates an rdf representation of letter used to load into the triple store
      '''
    def create_rdf_letter (self, letters):
 
        for l in letters:
            correspondence = base_uri + "letters/view/" + l.type + '/' + urllib.quote(l.correspondent) + '/' + str(l.id)
            self.add_author(correspondence, "Charles Dickens")
            
            self.add_time(correspondence, str(l.letter_date)+'T00:00:00')
            self.add_correspondent(correspondence, l.correspondent)

            self.add_salutation(correspondence, l.correspondent, l.salutation)
                #this section will parse for proper names in due course
                #commented out whilst code is being ported
                #letter_name = parse_text.parseProperNames(text)
               # print"names, ", letter_name
                
                #for name in letter_name:
                #    letter_rdf += "<letter:personReferred>%s</letter:personReferred>" %(name)
                                   
            letter_quotes = parse_text.parse_balanced_quotes(l.letter_text)
            for quote in letter_quotes:
                 if str(quote[0:1]).isupper and "!" not in quote:
                     self.add_text(correspondence, parse_text.stripPunc(quote))
                
        letter_rdf = self.g.serialize(format="pretty-xml", max_depth=3)
        return letter_rdf
    
    ''' function to create an endpoint in rdf/xml '''
    def create_rdf_end (self):

        correspondence = base_uri 
        
        letter = {}  
        letter = dbase.get_endpoint_rdf()
    
        letter_items = letter.items()
        letter_items.sort()
          
        for url, text in letter_items:
            correspondence = base_uri + "letters/view/dickens/" + urllib.quote(text[1]) + '/' + str(url)
            self.add_author(correspondence, "Charles Dickens")
            
            self.add_time(correspondence, str(text[3])+'T00:00:00')
            self.add_correspondent(correspondence, urllib.quote(str(text[1])))
            self.add_salutation(correspondence, urllib.quote(str(text[1])), str(text[4]))
            #this section will parse for proper names in due course
            #commented out whilst code is being ported
            #letter_name = parse_text.parseProperNames(text)
           # print"names, ", letter_name
            
            #for name in letter_name:
            #    letter_rdf += "<letter:personReferred>%s</letter:personReferred>" %(name)
           # works = Set(["Copperfield", "David Copperfield"])                
            letter_quotes = parse_text.parse_balanced_quotes(text[2])
            for quote in letter_quotes:
                #the length is to remove anything really long
                #if str(quote[0:1]).isupper and "!" not in quote and len(str(quote)) < 40:
                self.add_text(correspondence, parse_text.stripPunc(quote))
                #if quote in works:
                #    self.add_author_text(correspondence, parse_text.stripPunc(quote))
                #else:
                #    self.add_text(correspondence, parse_text.stripPunc(quote))

        letter_rdf = self.g.serialize(format="pretty-xml", max_depth=3)
        return letter_rdf
        
    def create_correspondent(self, corr, letter_items):
            u_corr = unicode(corr)
            
            correspondence = base_uri + "letters/correspondent/" + urllib.quote(corr)
            
            self.add_correspondent(correspondence, corr)
    
            for url, text in letter_items:
                if url is not None or url != '':
                    self.add_salutation(correspondence, corr, str(url))
            
            letter_rdf = self.g.serialize(format="pretty-xml", max_depth=3)
            
            return letter_rdf
        
    ''' function to add author to graph '''
    def add_author(self, correspondence, name):
            
        dc_author = urllib.quote(name)
        lauthor = URIRef(base_uri+ 'author/%s' % dc_author)
        self.g.add((correspondence, dublin_core['author'], Literal(name)))

        return lauthor
    
    ''' function to add salutation to graph '''
    def add_salutation(self, correspondence, author, name):
        
        nameid = urllib.quote(author)
        person = URIRef(base_uri + 'view/dickens/correspondent/%s' % nameid)
        #self.g.add((person, RDF.type, FOAF['nick']))
        self.g.add((correspondence, FOAF['nick'], Literal(name)))
        
        return person
    
    ''' function to add correspondent to graph '''
    def add_correspondent(self, correspondence, name):
        
        nameid = urllib.quote(name)
        person = URIRef(base_uri + 'view/dickens/correspondent/%s' % nameid)
        self.g.add((correspondence, letter_ns["correspondent"], Literal(name)))
        #self.g.add((person, Letter, Literal(name)))
        
        return person
    
    ''' function to add referred text to the graph'''
    def add_text (self, correspondence, textname):

        textid = urllib.quote(textname)
        book = URIRef(base_uri + 'book/%s' % textid)
        self.g.add((correspondence, letter_ns['textReferred'], Literal(textname)))  
        #self.g.add((book, Letter["textReferred"], Literal(textname)))       
        return book
    
    ''' function to add author referred text to the graph'''
    def add_author_text (self, correspondence, textname):

        textid = urllib.quote(textname)
        book = URIRef(base_uri + 'book/%s' % textid)
        self.g.add((correspondence, letter_ns['textAuthorReferred'], Literal(textname)))  
        #self.g.add((book, Letter["textReferred"], Literal(textname)))       
        return book
    
    ''' function to add time '''
    def add_time(self, correspondence, time):
        
        owl = URIRef(base_uri + 'date/%s' % time)
        self.g.add((correspondence, owl_time['inCalendarClockDataType'], Literal(str(time))))
        return owl