try:
    import json
except ImportError:
    import simplejson as json

class json_transform:
  

    '''
    Function to return the text as json
    '''
    def to_dict (self, letterobj, type):

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

    def jsonify (self, output):
        return json.dumps(output, sort_keys = True, indent=4)