from openletters.model import dbase
from openletters.parseText import parse_text

import rdflib
from rdflib import Namespace
from rdflib.graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace
from rdflib import RDF, RDFS
from rdflib.store import Store, NO_STORE, VALID_STORE


letter_ns = Namespace('http://purl.org/letter#')
Letter = URIRef(letter_ns['Letter'])
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
XSD_NS = Namespace(u'http://www.w3.org/2001/XMLSchema#')
base_uri = "http://www.opencorrespondence.org/schema"


'''
  creates an rdf representation of letter used to load into the triple store
  @param uri 
  @return letter_rdf
  '''
def createRdfLetter (uri):

    letter_rdf = '<rdf:RDF\n'
    letter_rdf += 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
    letter_rdf += 'xmlns:letter="http://purl.org/letter"\n'
    letter_rdf += 'xmlns:foaf="http://xmlns.com/foaf/0.1"\n'
    letter_rdf += 'xmlns:dc ="http://purl.org/dc/elements/1.1/">\n'
    letter_rdf += '<dc:author>Charles Dickens</dc:author>'
    
    letter = {}  
    letter = dbase.getLetterText(uri)
    letter_items = letter.items()
    letter_items.sort()

    for url, text in letter_items:
        #letter_name = parse_text.parseProperNames(text)
       # print"names, ", letter_name
        
        #for name in letter_name:
        #    letter_rdf += "<letter:personReferred>%s</letter:personReferred>" %(name)
                           
        letter_quotes = parse_text.parse_balanced_quotes(text)
        for quote in letter_quotes:
            if str(quote[0:1]).isupper and "!" not in quote:
                letter_rdf += "<letter:textReferred>%s</letter:textReferred>\n" %(parse_text.stripPunc(quote))

    letter_rdf += "</rdf:RDF>"
    return letter_rdf

def create_store ():
    
    letter = URIRef(base_uri + 'letter#%s' % id)
    #set up MySQL store - need to set up a user
    store = rdflib.plugin.get('MySQL', Store)("root")
    graph = Graph(store)
    # Bind a few prefix, namespace pairs.
    graph.bind('dc', 'http://http://purl.org/dc/elements/1.1/')
    graph.bind('foaf', 'http://xmlns.com/foaf/0.1/')
    graph.bind('letter', 'http://purl.org/letter')
    graph.add(letter, RDF.type, self.Letter)
    
    graph.add((letter, letter_ns['personReferred'], m_quote))
    graph.commit()
    
    