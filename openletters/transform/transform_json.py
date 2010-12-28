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
            dict += "index: {"
        else:
            dict += "letter: {"
         
        for l in letterobj:
            
            dict +=  str(l.id) + ': [ {'
            dict += '"author": "' + l.type
            dict += '", "correspondent: "' + l.correspondent
            dict += ', "date": "' + l.letter_date
            
            if l.letter_text:
                #remove the brackets in the letter
                text = l.letter_text.replace("[", "").replace("]", "")
                dict += '", "text": "' + text
            
            dict += '"}],'
        
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
        
        for u, book in book_items:

            dict +=  str(title) + ': [ '
            dict += '"title": "' + u
            dict += '"author": "' + author
            dict += '", "start: "' + book[0]
            dict += '", "end: "' + book[1]
            dict += '", "abstract: "' + book[2]
                     
            if type == "book":
               dict += '", "source: http://gutenberg.org/ebooks/"' + book[4]
            
            dict +=   '", "sameas: "' + u"http://dbpedia.org/page/" + book[3] 
            
            dict += '"]'
        
        dict += '}'

        return self.jsonify(dict)
    
    def jsonify (self, output):
        return json.dumps(output, sort_keys = True, indent=4)