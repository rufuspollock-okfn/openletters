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

from openletters.model import dbase
from openletters.parse import parse_text

letter_ns = Namespace('http://www.opencorrespondence.org/schema#')
skos = Namespace('http://www.w3.org/2008/05/skos#')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
XSD_NS = Namespace(u'http://www.w3.org/2001/XMLSchema#')
owl_time = Namespace('http://www.isi.edu/~pan/damltime/time-entry.owl#')
dublin_core = Namespace('http://purl.org/dc/elements/1.1/')
owl = Namespace('http://www.w3.org/2002/07/owl#')
exam = Namespace('http://example.org/')
geo = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')


base_uri = "http://www.opencorrespondence.org/"

class rdf_transform:
    
    def __init__(self):
        
        self.g = Graph('IOMemory')
        self.g.bind('dc', dublin_core)
        self.g.bind('foaf', FOAF)
        self.g.bind('time-entry', owl_time)
        self.g.bind('letter', letter_ns)
        self.g.bind('owl', owl)
        self.g.bind('ex', exam)
        self.g.bind('geo', geo)
        self.g.bind('base', base_uri)


    def create_rdf_letter (self, letters):
        '''
          creates an rdf representation of letter used to load into the triple store
        '''
        for l in letters:
            correspondence = base_uri + "letters/resource/" + l.type + '/' + urllib.quote(l.correspondent) + '/' + str(l.id)
            self.add_author(correspondence, "Charles Dickens")
            self.add_subject(correspondence, "letter")
            self.add_time(correspondence, str(l.letter_date)+'T00:00:00')
            self.add_correspondent(correspondence, l.correspondent)
            #self.add_place(correspondence, parse_text.find_geographical(l.letter_text))
            try:
                place = parse_text.find_geographical(str(l.letter_text))
            #unicode errors are text related
            except UnicodeError:
                pass
            if place is not None:
                self.add_place(correspondence, place)
                
            self.add_letter_text(correspondence, l.letter_text)
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
                     if quote == "ALL THE YEAR ROUND" or quote=="HOUSEHOLD WORDS" or quote== "Household Words":
                         self.add_magazine(correspondence, parse_text.stripPunc(quote))
                     else:
                         self.add_text(correspondence, parse_text.stripPunc(quote))
                
        letter_rdf = self.g.serialize(format="pretty-xml", max_depth=3)
        return letter_rdf
    
    
    def create_rdf_end (self):
        ''' function to create an endpoint in rdf/xml '''
        correspondence = base_uri 
        
        letter = {}  
        letter = dbase.get_endpoint_rdf()
    
        letter_items = letter.items()
        letter_items.sort()
    
        works = set()
        works = dbase.get_books()
        
        for url, text in letter_items:
            try:
                correspondence = base_uri + "letters/resource/dickens/" + urllib.quote(text[1]) + '/' + str(url)
                self.add_author(correspondence, "Charles Dickens")
                self.add_subject(correspondence, "letter")
                self.add_subject(correspondence, "Charles Dickens")
                self.add_subject(correspondence, parse_text.camel_case(str(text[1])))
                self.add_time(correspondence, str(text[3])+'T00:00:00')
                self.add_correspondent(correspondence, urllib.quote(parse_text.camel_case(str(text[1]))))
                self.add_salutation(correspondence, urllib.quote(str(text[1])), str(text[4]))
                place = parse_text.find_geographical(str(text[2]))
                letter = str(text[2])
            #unicode errors are text related
            except UnicodeError:
                pass
            if place is not None:
                self.add_place(correspondence, place)
            
            self.add_letter_text(correspondence, letter)
            
            #this section will parse for proper names in due course
            #commented out whilst code is being ported
            #letter_name = parse_text.parseProperNames(text)
           # print"names, ", letter_name 
                           
            letter_quotes = parse_text.parse_balanced_quotes(text[2])
            for quote in letter_quotes:
                work = parse_text.stripPunc(quote)

                #TODO: Normalise the text to reduce code repetition
                periodicals = set(['All The Year Round', 'Household Words', 'The Daily News'])
                #print "quote", parse_text.stripPunc(quote)
                if quote in periodicals:
                    self.add_magazine(correspondence, quote)
                
                if work in works:
                    if work == "Copperfield":
                        work = "David Copperfield"
                    elif work == "Nickleby":
                        work = "Nicholas Nickleby"
                    elif work == "Edwin Drood":
                        work = "The Mystery of Edwin Drood" 
                    elif work == "Dombey":
                        work = "Dombey and Son" 
                    elif work == "Tale of Two Cities":
                        work = "A Tale of Two Cities"
                    elif work == "Christmas Carol":
                        work = "A Christmas Carol"
                        
                    self.add_text(correspondence, work)

        letter_rdf = self.g.serialize(format="pretty-xml", max_depth=3)
        return letter_rdf
        
    def create_correspondent(self, corr, letter_items):
            u_corr = unicode(corr)

            correspondence = base_uri + "correspondent/resource/" + urllib.quote(corr)
            self.add_subject(correspondence, "correspondent")
            #self.add_correspondent(correspondence, corr)
    
            for url, text in letter_items:
                if url is not None or url != '':
                    self.add_salutation(correspondence, corr, str(url))
            #need rules to define relationships - family, authors
            if u_corr == "Miss Hogarth":
                self.add_subject(correspondence, "daughter")
                self.add_daughter(correspondence, "Charles Dickens")
                self.add_sameas(correspondence, "http://dbpedia.org/page/Georgina_Hogarth")
                
            letter_rdf = self.g.serialize(format="pretty-xml", max_depth=3)
            
            return letter_rdf
        
    def create_publication(self, title, type):
            books_set = {}
            start = '';
            end = '';
            abstract = '';
            uri_str = '';

            if type == "magazine":
                if title == "Household Words":
                     start = u"1850-03-01"
                     end = u"1859-05-01"
                     abstract = u"Household Words was an English weekly magazine edited by Charles Dickens in the 1850s which took its name from the line from Shakespeare 'Familiar in his mouth as household words' - Henry V"
                     uri_str = u"Household_Words"
                elif title =="All the Year Round":
                     start = u"1859-01-28"
                     end = u"1895-03-30"
                     abstract = u"All the Year Round was a Victorian periodical, being a British weekly literary magazine founded and owned by Charles Dickens, published between 1859 and 1895 throughout the United Kingdom. Edited by Dickens, it was the direct successor to his previous publication Household Words, abandoned due to differences with his former publisher. It hosted the serialization of many prominent novels, including Dickens' own A Tale of Two Cities. After Dickens's death in 1870, it was owned and edited by his eldest son Charles Dickens, Jr." 
                     uri_str = u"All_the_Year_Round"
            else:
                books = dbase.get_book_rdf(title)
                book_items = books.items()
                book_items.sort()
                
                for u, book in book_items:

                    title = u
                    start = book[0]
                    end = book[1]
                    abstract = book[2]
                    uri_str = book[3]
                    source = book[4]
                    #create a books dictionary as a list of records to build a list of uris from
                    # title => uri string
                    books_set[u] = uri_str
                    
                    if ":" in u:
                        for bk in u.split(":"):
                            books_set[bk[0]] = uri_str
            
                    if "The " in u or "A " in u:
                        aka = u.replace("The ", "").replace("A ", "")
                        books_set[aka] = uri_str
            
            correspondence = base_uri + type + "/resource/" + title.strip().replace(" ", "_")
            self.add_subject(correspondence, type)
            self.add_subject(correspondence, "Charles Dickens")
            self.add_author(correspondence, "Charles Dickens")    
            self.add_time(correspondence, start)
            self.add_time(correspondence, end)
            self.add_title(correspondence, title)
                
            self.add_abstract(correspondence, abstract)
            uri = u"http://dbpedia.org/page/" + uri_str
            self.add_sameas(correspondence, uri)
            
            if type == "book":
               source_uri = "http://gutenberg.org/ebooks/" + source
               self.add_sameas(correspondence, source_uri)
            
            letter_rdf = self.g.serialize(format="pretty-xml", max_depth=3)
            
            return letter_rdf
        
    def create_place (self, place):
        
        (long, lat, place_name, place_abstract) = ('','','','')
       # long = ''
       # lat = ''
       # place_name = ''
       # place_abstract = ''

        if place == "Gads Hill":
            long = '51.2440N'
            lat = '0.2728E'
            place_name = place
            place_abstract = "Gads Hill Place in Higham, Kent, sometimes spelt Gadshill Place and Gad's Hill Place, was the country home of Charles Dickens, the most successful British author of the Victorian era."
        elif place == 'Tavistock House':
            long = '51.5255N'
            lat = '0.1286W'
            place_name = place
            place_abstract = "Tavistock House was the London home of the noted British author Charles Dickens and his family from 1851 to 1860. At Tavistock House Dickens wrote Bleak House, Hard Times, Little Dorrit and A Tale of Two Cities. He also put on amateur theatricals there which are described in John Forster's Life of Charles Dickens. Later, it was the home of William and Georgina Weldon, whose lodger was the French composer Charles Gounod, who composed part of his opera Polyeucte at the house."
            
        correspondence = base_uri + "place/resource/" + urllib.quote(place)
        self.add_latitude(correspondence, lat)
        self.add_longitude(correspondence, long)
        self.add_place_name(correspondence, place_name)
        self.add_description(correspondence, place_abstract)
        
        letter_rdf = self.g.serialize(format="pretty-xml", max_depth=3)
        
        return letter_rdf

    def create_author (self, data):
        '''
           function to return an author graph in rdf
        '''
        author = u"Charles Dickens"
        subject = u"author"
        born = u"1812-02-07"
        died = u"1870-06-09"
        abstract = u"Charles John Huffam Dickens, pen-name 'Boz', was the most popular English novelist of the Victorian era, and one of the most popular of all time, responsible for some of English literature's most iconic characters. Many of his novels, with their recurrent theme of social reform, first appeared in periodicals and magazines in serialised form, a popular format for fiction at the time. Unlike other authors who completed entire novels before serial production began, Dickens often wrote them while they were being serialized, creating them in the order in which they were meant to appear. The practice lent his stories a particular rhythm, punctuated by one 'cliffhanger' after another to keep the public looking forward to the next installment. The continuing popularity of his novels and short stories is such that they have never gone out of print. His work has been praised for its mastery of prose and unique personalities by writers such as George Gissing and G. K. Chesterton, though the same characteristics prompted others, such as Henry James and Virginia Woolf, to criticize him for sentimentality and implausibility."
        author_url = u"http://en.wikipedia.org/wiki/Charles_Dickens"
        
        correspondence = base_uri + "author/resource/" + author
        self.add_subject(correspondence, "Charles Dickens")
        self.add_subject(correspondence, "author")
        self.add_nick(correspondence, "Boz")
        self.add_time(correspondence, born)
        self.add_time(correspondence, died)
        self.add_text(correspondence, abstract)
        self.add_sameas(correspondence, author_url)
        
        letter_rdf = self.g.serialize(format="pretty-xml", max_depth=3)
        
        return letter_rdf
        
    
    def add_author(self, correspondence, name):
        ''' function to add author to graph '''  
        dc_author = urllib.quote(name)
        lauthor = URIRef(base_uri+ 'author/resource/%s' % dc_author)
        self.g.add((correspondence, dublin_core['creator'], lauthor))
        #self.g.add((correspondence, dublin_core['creator'], Literal(name)))
        return lauthor
    

    def add_salutation(self, correspondence, author, name):
        ''' function to add salutation to graph '''        
        nameid = urllib.quote(author)
        person = URIRef(base_uri + 'correspondent/resource/%s' % nameid)
        #self.g.add((person, RDF.type, FOAF['nick']))
        self.g.add((correspondence, FOAF['nick'], Literal(name)))
        
        return person
    

    def add_correspondent(self, correspondence, name):
        ''' function to add correspondent to graph '''        
        nameid = urllib.quote(name)
        person = URIRef(base_uri + 'correspondent/resource/%s' % nameid)
        self.g.add((correspondence, letter_ns["correspondent"], person))
        #self.g.add((person, Letter, Literal(name)))
        
        return person
    

    def add_magazine(self, correspondence, name):
        ''' function to add magazine to graph '''       
        nameid = urllib.quote(name)
        magazine = URIRef(base_uri + 'magazine/resource/%s' % nameid)
        self.g.add((correspondence, letter_ns['textReferred'], magazine))
        #self.g.add((person, Letter, Literal(name)))
        
        return magazine
    

    def add_text (self, correspondence, textname):
        ''' function to add referred text to the graph'''
        textid = base_uri + "book/resource/"+textname.replace("\n", "_").replace(" ", "_")
        return self.g.add((correspondence, letter_ns['textReferred'], URIRef(textid)))        
    
    
    def add_author_text (self, correspondence, textname):
        ''' function to add author referred text to the graph'''
        textid = urllib.quote(textname)
        self.g.add((correspondence, letter_ns['textAuthorReferred'], Literal(textname)))        
        return book
        
    def add_place(self, correspondence, place):
        return self.g.add((correspondence, dublin_core['date'], Literal(str(time))))
    
    def add_subject (self, correspondence, subject):
        return self.g.add((correspondence, dublin_core['subject'], Literal(subject))) 
    
    def add_sameas (self, correspondence, link):
        return self.g.add((correspondence, owl['sameAs'], URIRef(link)))
    
    
    def add_time(self, correspondence, time):
        ''' function to add time '''
        return self.g.add((correspondence, dublin_core['date'], Literal(str(time))))

    def add_title (self, correspondence, title):
        return self.g.add((correspondence, dublin_core['title'], Literal(title)))
    
    def add_nick (self, correspondence, nick):
        return self.g.add((correspondence, FOAF['nick'], Literal(nick)))
    
    def add_place (self, correspondence, place):
        return self.g.add((correspondence, dublin_core['title'], URIRef(base_uri + "place/resource/"+urllib.quote(place))))
        
    def add_daughter (self, correspondence, author):
        return self.g.add((correspondence, exam['daughter'], URIRef(base_uri + "author/resource/" + author)))
    
    def add_letter_text (self, correspondence, letter_text):
        return self.g.add((correspondence, letter_ns['Text'], Literal(letter_text)))
    
    def add_longitude (self, correspondence, long):
        return self.g.add((correspondence, geo['long'], Literal(long)))
    
    def add_latitude (self, correspondence, lat):
        return self.g.add((correspondence, geo['lat'], Literal(lat)))
    
    def add_description (self, correspondence, abstract):
        return self.g.add((correspondence, geo['desc'], Literal(abstract)))
    
    def add_place_name (self, correspondence, name):
        return self.g.add((correspondence, geo['name'], Literal(name)))
    
    def add_abstract (self, correspondence, letters):
        return self.g.add((correspondence, letter_ns['text'], Literal(letters)))