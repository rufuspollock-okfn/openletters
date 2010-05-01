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
    
    letter_rdf = ''
    letter_quotes = []
    
    letter = {}
    letter = dbase.getLetterText(uri)
    
    letter_items = letter.items()
    letter_items.sort()

    letter_tok = []
    for url, text in letter_items:
        #tokenise here for future methods - shld probably use the tokenise inbuilt
        letter_tok = str(text[0]).split(" ")
        letter_rdf = '<rdf:RDF>'
        letter_name = parse_text.parseProperNames(letter_tok)
        for name in letter_name:
            
            letter_rdf += "<letter:personReferred>%s</letter:personReferred>" %(name)
                           
        letter_quotes = parse_text.parseBalancedQuotes(str(text[0]))
        for quote in letter_quotes:
            #graph.add((letter, letter_ns['textReferred'], quote))
            letter_rdf += "<letter:personReferred>%s</letter:personReferred>" %(quote)
    
    #graph.commit()
    #letter_rdf = graph.serialize()
    letter_rdf = "</rdf:RDF>"
    return letter_rdf

def create_store ():
    
    letter = URIRef(base_uri + 'letter#%s' % id)
    #set up MySQL store - need to set up a user
    store = rdflib.plugin.get('MySQL', Store)()
    graph = Graph(store)
    # Bind a few prefix, namespace pairs.
    graph.bind('dc', 'http://http://purl.org/dc/elements/1.1/')
    graph.bind('foaf', 'http://xmlns.com/foaf/0.1/')
    graph.add(letter, RDF.type, self.Letter)
    
    graph.add((letter, letter_ns['personReferred'], m_quote))
    