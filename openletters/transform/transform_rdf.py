from openletters.model import dbase
from openletters.parseText import parse_text

import urllib
#import rdflib
#from rdflib.graph import ConjunctiveGraph as Graph
#from rdflib import plugin
#from rdflib.store import Store, NO_STORE, VALID_STORE
#from rdflib import Namespace
#from rdflib import Literal
#from rdflib import URIRef


#letter_ns = Namespace('http://purl.org/letter#')
#Letter = URIRef(letter_ns['Letter'])
#FOAF = Namespace('http://xmlns.com/foaf/0.1/')
#XSD_NS = Namespace(u'http://www.w3.org/2001/XMLSchema#')
#owl_time = Namespace('http://www.isi.edu/~pan/damltime/time-entry.owl#')
#dublin_core = Namespace('http://purl.org/dc/elements/1.1/')
#base_uri = "http://www.opencorrespondence.org/schema"


'''
  creates an rdf representation of letter used to load into the triple store
  @param uri 
  @return letter_rdf
  '''
def createRdfLetter (uri):
#uses OWL, FOAF, DC and letter Purl schemas
    letter_rdf = '<rdf:RDF\n'
    letter_rdf += 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
    letter_rdf += 'xmlns:letter="http://purl.org/letter/"\n'
    letter_rdf += 'xmlns:time-entry="http://www.isi.edu/~pan/damltime/time-entry.owl#"\n'
    letter_rdf += 'xmlns:foaf="http://xmlns.com/foaf/0.1/"\n'
    letter_rdf += 'xmlns:dc ="http://purl.org/dc/elements/1.1/"\n'
    letter_rdf += 'xml:base="http://www.opencorrespondence.org/" >\n'
    
    letter_rdf += '<rdf:Description rdf:about="letter/text?letter='+uri+'">'
    letter_rdf += '<dc:author>Charles Dickens</dc:author>'
        
    letter = {}  
    letter = dbase.get_letter_rdf(uri)
    
    letter_items = letter.items()
    letter_items.sort()
    
    for url, text in letter_items:
        letter_rdf += '<time-entry:inCalendarClockDataType rdf:datatype="xsd:dateTime">'+str(text[3])+'T00:00:00</time-entry:inCalendarClockDataType>'
        #still need to put in a foaf:Person link for the person - we have potential nickname data in the db
        
        letter_rdf += '<letter:Correspondent>'+str(text[1])+'</letter:Correspondent>'
        #this section will parse for proper names in due course
        #commented out whilst code is being ported
        #letter_name = parse_text.parseProperNames(text)
       # print"names, ", letter_name
        
        #for name in letter_name:
        #    letter_rdf += "<letter:personReferred>%s</letter:personReferred>" %(name)
                           
        letter_quotes = parse_text.parse_balanced_quotes(text[2])
        for quote in letter_quotes:
            if str(quote[0:1]).isupper and "!" not in quote:
                letter_rdf += "<letter:textReferred>%s</letter:textReferred>\n" %(parse_text.stripPunc(quote))
        
    letter_rdf += "</rdf:Description>"
    letter_rdf += "</rdf:RDF>"
    return letter_rdf

def create_rdf_end ():
    #default_graph_uri = "http://rdflib.net/rdfstore"
    #configString = "host=localhost,user=root,password=enoch,db=rdfstore"
    # Get the mysql plugin. You may have to install the python mysql libraries
    #store = plugin.get('MySQL', Store)('rdfstore')
    # Open previously created store, or create it if it doesn't exist yet
    #rt = store.open(configString, create=False)
    #if rt == NO_STORE:
    # There is no underlying MySQL infrastructure, create it
    #    store.open(configString,create=True)
    #else:
    #    assert rt == VALID_STORE,"The underlying store is corrupted"
    # There is a store, use it
    #graph = Graph(identifier = URIRef(default_graph_uri))
#uses OWL, FOAF, DC and letter Purl schemas
    letter_rdf = '<rdf:RDF\n'
    letter_rdf += 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
    letter_rdf += 'xmlns:letter="http://purl.org/letter/"\n'
    letter_rdf += 'xmlns:time-entry="http://www.isi.edu/~pan/damltime/time-entry.owl#"\n'
    letter_rdf += 'xmlns:foaf="http://xmlns.com/foaf/0.1/"\n'
    letter_rdf += 'xmlns:dc ="http://purl.org/dc/elements/1.1/"\n'
    letter_rdf += 'xml:base="http://www.opencorrespondence.org/" >\n'
    
    
    letter = {}  
    letter = dbase.get_endpoint_rdf()

    letter_items = letter.items()
    letter_items.sort()
    
    
    for url, text in letter_items:
        print url
        letter_rdf += '<rdf:Description rdf:about="letters/text?letter='+ str(text[0])+'">\n'
        letter_rdf += '<dc:author>Charles Dickens</dc:author>\n'
        #graph.add((owl_time, owl_time['inCalendarClockDataType'], Literal(str(text[3])+'T00:00:00')))
        #graph.add(dublin_core, dublin_core['author'], Literal('Charles Dickens'))
        #graph.add(Letter, Letter['Correspondent'], Literal(str(text[1])))
        
        letter_rdf += '<time-entry:inCalendarClockDataType rdf:datatype="xsd:dateTime">'+str(text[3])+'T00:00:00</time-entry:inCalendarClockDataType>\n'
        #still need to put in a foaf:Person link for the person - we have potential nickname data in the db
        
        letter_rdf += '<letter:Correspondent rdf:resource="/data/correspondent?corr='+urllib.quote(str(text[1]))+'" />\n'
        letter_rdf += '<foaf:nick>'+str(text[4])+'</foaf:nick>\n'
        
        #this section will parse for proper names in due course
        #commented out whilst code is being ported
        #letter_name = parse_text.parseProperNames(text)
       # print"names, ", letter_name
        
        #for name in letter_name:
        #    letter_rdf += "<letter:personReferred>%s</letter:personReferred>" %(name)
                           
        letter_quotes = parse_text.parse_balanced_quotes(text[2])
        for quote in letter_quotes:
            #the length is to remove anything really long
            if str(quote[0:1]).isupper and "!" not in quote and len(str(quote)) < 40:
                #graph.add(Letter, Letter['textReferred'], Literal(parse_text.stripPunc(quote)))
                letter_rdf += "<letter:textReferred>%s</letter:textReferred>\n" %(parse_text.stripPunc(quote))
        
        letter_rdf += "</rdf:Description>"
        
    letter_rdf += "</rdf:RDF>"
    #letter_rdf = graph.serialize
    return letter_rdf
    
def create_correspondent(corr):
        u_corr = urllib.unquote(corr)
        
        letter_rdf = '<rdf:RDF\n'
        letter_rdf += 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
        letter_rdf += 'xmlns:letter="http://purl.org/letter/"\n'
        letter_rdf += 'xmlns:time-entry="http://www.isi.edu/~pan/damltime/time-entry.owl#"\n'
        letter_rdf += 'xmlns:foaf="http://xmlns.com/foaf/0.1/"\n'
        letter_rdf += 'xml:base="http://www.opencorrespondence.org/data/correspondent" >\n'
        
        letter_rdf += '<rdf:Description rdf:about="?corr='+urllib.quote(corr)+'">\n'       
        letter_rdf += '<letter:Correspondent>'+u_corr+'</letter:Correspondent>\n'
        
        letter = {}  
        letter = dbase.get_correspondent(u_corr)

        letter_items = letter.items()
        letter_items.sort()

        for url, text in letter_items:
            letter_rdf += "<foaf:nick>%s</foaf:nick>\n" %(str(url))
        
        letter_rdf += '</rdf:Description>'
        letter_rdf += '</rdf:RDF>'
        
        return letter_rdf
    