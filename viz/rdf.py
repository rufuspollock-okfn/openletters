'''Load Dickens data as RDF and do some analysis.

This is more an exercise in using RDF -- you could accomplish the analysis much
more easily directly.
'''
import rdflib
from rdflib import Namespace
from rdflib.Graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace
from rdflib import RDF, RDFS
from rdflib.store.IOMemory import IOMemory
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
XSD_NS = Namespace(u'http://www.w3.org/2001/XMLSchema#')

from dickens import load_json


PATH = 'dickens.nt'
letter_ns = Namespace('http://purl.org/letter#')
base_uri = 'http://rufuspollock.org/code/dickens/'
Letter = URIRef(letter_ns['Letter'])
class LoadToRdf(object):

    def __init__(self):
        self.graph = Graph(store=IOMemory())
        # Bind a few prefix, namespace pairs.
        self.graph.bind('dc', 'http://http://purl.org/dc/elements/1.1/')
        self.graph.bind('foaf', 'http://xmlns.com/foaf/0.1/')

    def json_to_rdf(self):
        person_dict = {}

        dickens = self.add_person(DICKENS)
        self.graph.add((self.Letter, RDF.type, RDFS.Class))
        self.graph.add((self.Letter, RDFS.label, Literal('A postal letter')))
        for name,year in load_json():
            if name in person_dict:
                person = person_dict[name]
            else:
                person = self.add_person(name)
                person_dict[name] = person
            self.add_letter(person, dickens, year, id)
        self.graph.commit()
        print 'Writing RDF data to %s' % PATH
        self.graph.serialize(open(PATH,'w'), format='nt')

    def add_person(self, name):
        nameid = name.lower().replace(' ', '_').replace('.', '')
        person = URIRef(base_uri + 'person#%s' % nameid)
        self.graph.add((person, RDF.type, FOAF['Person']))
        self.graph.add((person, FOAF['name'], Literal(name)))
        return person

    def add_letter(self, to, from_, date, id):
        letter = URIRef(base_uri + 'letter#%s' % id)
        self.graph.add((letter, RDF.type, self.Letter))
        self.graph.add((letter, letter_ns['to'], to))
        self.graph.add((letter, letter_ns['from'], from_))
        self.graph.add((letter, letter_ns['date'], Literal(date)))
        return letter


import matplotlib.pyplot as plt
class Analyzer(object):
    '''Analyze the Dickens letter data.

    !! SPARQL does not support aggregates so we have to do this by hand.
    '''
    # see add_person above
    dickens = URIRef(base_uri + 'person#mr_charles_dickens')

    def __init__(self):
        self.graph = Graph(store=IOMemory())
        self.graph.parse(PATH, format='nt')

    def info(self): 
        print len(self.graph)

    def simple_search(self):
        for count,(s,p,o) in enumerate(
                # self.graph.triples((self.dickens, letter_ns['from'],None))
                # self.graph.triples((self.dickens,None,None))
                self.graph.triples((None, letter_ns['from'], self.dickens))
                ):
            if count > 10:
                break
            print s,p,o

    def plot_counts(self):
        q = '''SELECT ?adate
               WHERE {
                  ?a letter:date ?adate .
                  ?a letter:from <%s> .
               }''' % (self.dickens)
        spar = self.graph.query(q, initNs=dict(letter=letter_ns))
        dates = [ row[0].toPython() for row in spar ]
        bins = range(min(dates), max(dates)+1)
        plt.hist(dates, bins, fc='blue', alpha=0.8)
        plt.savefig('letter_dates.png')

    def plot_letter_network(self):
        q = '''SELECT ?adate ?to
               WHERE {
                  ?a letter:date ?adate .
                  ?a letter:from <%s> .
                  ?a letter:to ?b .
                  ?b foaf:name ?to .
               }''' % (self.dickens)
        spar = self.graph.query(q, initNs=dict(letter=letter_ns, foaf=FOAF))
        values = [ [row[0].toPython(), unicode(row[1]) ] for row in spar ]
        names = list(set([ x[1] for x in values ]))
        import networkx as nx
        dgr = nx.Graph()
        labels = { -1: u'Charles Dickens' } 
        for count,name in enumerate(names):
            # dgr.add_edge(u'Charles Dickens', name)
            dgr.add_edge(-1, count)
            labels[count] = name
        pos = nx.graphviz_layout(dgr, prog='twopi')
        fig = plt.figure(1, figsize=(15,15))
        nx.draw(dgr, pos, node_size=15, labels=labels, font_size=10)
        plt.savefig('dickens_letter_network.png')


if __name__ == '__main__':
    # converter = LoadToRdf()
    # converter.json_to_rdf()
    a = Analyzer()
    a.info()
    a.plot_letter_network()

