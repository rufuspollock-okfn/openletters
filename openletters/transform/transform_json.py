try:
    import json
except ImportError:
    import simplejson as json
    
from openletters.model import dbase
from openletters.parse import parse_text


class json_transform:
  

    '''
    Function to return the text as json
    '''
    def to_dict (self, letterobj, type = ''):

        dict = '{'
        
        if type is None:
            dict += "letter: {"
        else:
            dict += "http://www.tei-c.org/ns/1.0: {: {"
            dict += "teiHeader: [{"
            dict += "titleStmt: [{" 
            
            #begin titleStmt
            dict += "title: Letter from Charles Dickens,"
            dict += "author: ,"
            dict += "editor: The Open Knowledge Foundation,"
            dict += "respStmt:{[ "
            dict += "resp: ,"
            dict += "name:,"
            dict += ']}'
            dict += "extent: Less than 1Mb ]}"
            dict += ']}'
            #end titleStmt
              
            #begin sourceDesc
            dict += "sourceDesc: [{"
            dict += "p: Digitised from Project Gutenberg, "
            dict += "bibl: [{"
            dict += "title: The Letters of Charles Dickens, "
            dict += "author: Charles Dickens,"
            dict += "editor: Mamie Dickens and Georgina Hogarth,"
            dict += "publisher: Chapman and Hall,"
            dict += "pubPlace: London,"
            dict += "date: 1870,"
            dict += ']}'
            dict += "]}"
            #end sourceDesc
            
            dict += 'encodingDesc: {['
            dict += 'projectDesc:Open Correspondence is a project to mine the social network of Nineteenth century letters. As part of the project it aims to provide the letters in various forms such as XML, JSON and RDF, '
            dict += 'editorialDecl: Some diphthongs (such  as \'ae\') have been modernised.,'
            dict += 'samplingDecl: An attempt has been made to encode the letters as they are in the original file. Work still needs to be done on the annotations.'
            dict += ']}'
            # end encodingDesc
            
            #publication Stmt
            dict += 'publicationStmt: [{'
            dict += 'distributor: Open Correspondence project for The Open Knowledge Foundation'
            dict += 'address: [{ addrLine: www.opencorrespondence.org, }] },'
            dict += 'date: 2011,'
            dict += 'availability: This text is available under an Open Data licence (www.opendefinition.org),'
            dict += ']}'
            #end publication Stmt
            
            dict += ']}'
            #end teiHeader
         
        for l in letterobj:   
            #
            dict += 'div: [{'
            dict += 'head: [{ @name:' #head
            dict += '@date:' + l.letter_date + ']}'
            dict += 'opener: [{ dateLine:' #opener
            dict += 'salutation:' +l.correspondent + ']}'
            
            text = l.letter_text.replace("[", "").replace("]", "")
            
            dict += 'text:' + text + ','
            dict += 'closer: [{ signature: \'dickens\' ]}' #signature
            dict += 'salutation:' + + ']}'
            dict += 'seg: [{ figure_entity:' + str(l.id) +',' #head
            dict += 'figureDesc:' + + ']}'
            dict += ']}'
            #end div

            
            #dict +=  str(l.id) + ': [ {'
            #dict += '"author": "' + l.type
            #dict += '", "correspondent: "' + l.correspondent
            #dict += ', "date": "' + l.letter_date
            
            #if l.letter_text:
                #remove the brackets in the letter
            #    text = l.letter_text.replace("[", "").replace("]", "")
            #    dict += '", "text": "' + text
            
            #dict += '"}],'
        
        #remove the last comma
        dict = dict[0: -1]
        
        dict += '} }'
            
        return self.jsonify(dict)
    
    '''
       Function to return json endpoint
    '''
    def to_end_dict (self):

        letter = dbase.get_endpoint_rdf()
        
        letter_items = letter.items()
        letter_items.sort()
        
        dict = '{'
        
        dict += '{ licence: This text is available as Open Data.  '
        
        dict += 'project: Open Correspondence is a project to mine the social network of Nineteenth century letters. As part of the project it aims to provide the letters in various forms such as XML, JSON and RDF '
        dict += 'editorial: Some diphthongs (such  as \'ae\') have been modernised.'
        dict += 'sampling: An attempt has been made to encode the letters as they are in the original file. Work still needs to be done on the annotations.}'
        dict += "index: {"
         
        for url, text in letter_items:
            
            dict +=  str(url) + ': [ {'
            dict += '"author": " Charles Dickens",'
            dict += '"correspondent: "' + str(text[1])
            dict += '", "date": "' + str(text[3])+'T00:00:00'
            
            letter_quotes = parse_text.parse_balanced_quotes(text[2])
            for quote in letter_quotes:
                dict += '", "text": "' + parse_text.stripPunc(quote)
            
            dict += '"}],'
        
        #remove the last comma
        dict = dict[0: -1]
        
        dict += '} }'
            
        return self.jsonify(dict)
    
    '''
    Function to return the text as json
    '''
    def corr_json (self, author, letterobj):

        dict = '{'
               
        dict += '{ licence: This text is available as Open Data.  '
        
        dict += 'project: Open Correspondence is a project to mine the social network of Nineteenth century letters. As part of the project it aims to provide the letters in various forms such as XML, JSON and RDF '
        dict += 'editorial: Some diphthongs (such  as \'ae\') have been modernised.'
        dict += 'sampling: An attempt has been made to encode the letters as they are in the original file. Work still needs to be done on the annotations.}'
        

        dict +=  str(author) + ': [ '
        dict += '"correspondent": "' + author

        for l, txt in letterobj:
            dict += '", "nick: "' + l
        
        dict += '"]'
        
        dict += '}'
            
        return self.jsonify(dict)

    '''
    Function to return the book graph
    '''
    def book_json (self, title, type):
        books_set = {}
        start = '';
        end = '';
        abstract = '';
        uri_str = '';
        source = '';

        author = "http://www.opencorrespondence.org/author/resource/Charles%20Dickens/json"
        books = dbase.get_book_rdf(title)
        book_items = books.items()
        book_items.sort()

        dict = '{'
        
        dict += '{ licence: This text is available as Open Data.  '
        
        dict += 'project: Open Correspondence is a project to mine the social network of Nineteenth century letters. As part of the project it aims to provide the letters in various forms such as XML, JSON and RDF '
        dict += 'editorial: Some diphthongs (such  as \'ae\') have been modernised.'
        dict += 'sampling: An attempt has been made to encode the letters as they are in the original file. Work still needs to be done on the annotations.}'
        
        for u, book in book_items:

            dict +=  str(title) + ': { '
            dict += '"title": "' + u
            dict += '"author": "' + author
            dict += '", "start: "' + book[0]
            dict += '", "end: "' + book[1]
            dict += '", "abstract: "' + book[2]
                     
            if type == "book":
               dict += '", "source: http://gutenberg.org/ebooks/"' + book[4]
            
            dict +=   '", "sameas: "' + u"http://dbpedia.org/page/" + book[3] 
            
            dict += '"}'
        
        dict += '}'

        return self.jsonify(dict)
    
    def create_place (self, placeobj):
        
        dict = '{'
        dict += '{ licence: This text is available as Open Data.  '
        
        dict += 'project: Open Correspondence is a project to mine the social network of Nineteenth century letters. As part of the project it aims to provide the letters in various forms such as XML, JSON and RDF '
        dict += 'editorial: Some diphthongs (such  as \'ae\') have been modernised.'
        dict += 'sampling: An attempt has been made to encode the letters as they are in the original file. Work still needs to be done on the annotations.}'
        
        
        for location in placeobj:
            dict +=  location.placeid + ': {'
            dict += '"latitude" :' +location.latitude
            dict += '"longitude" :' +location.longitude
            dict += '"source" :' + location.source + '}'
            
        dict += '}'
        
        return self.jsonify(dict)
    
    def jsonify (self, output):
        return json.dumps(output, sort_keys = True, indent=4)