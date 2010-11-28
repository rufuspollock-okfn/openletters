import re
import datetime as dtime

'''
   Parsing methods
'''

def parseCorrespondent (line):
        letter = ''
        correspondent = re.compile("(?=:).*", re.IGNORECASE)
        m = correspondent.match(line)
        if m:
            letter = m.group()
            return letter  

#Could be useful for FOAF
# needs tidying up - need to cast tuple to string to clean it up
def parseSalutation (n):
        sal = ''
        n = n.replace("MY", "").replace(",","")
        if "DEAREST" in n:
            sal = n.split("DEAREST")
        elif "DEAR" in n:
            sal = n.split("DEAR")  
        elif "RESPECTED" in n:
            sal = n.split("RESPECTED")
    
        return sal
    
def stripPunc (urlstring, type=''):
    urlstring = str(urlstring)
    ret_url = ''
    ret_url = urlstring.replace("]","")
    ret_url = ret_url.replace("[", "")
    ret_url = ret_url.replace(".", "")
    ret_url = ret_url.replace(": ", "")
    ret_url = ret_url.replace('"', "")
    ret_url = ret_url.replace(',', "")
    ret_url = ret_url.replace('\n', "")
    if type == "url":
        ret_url = ret_url.replace(" ", "")
        ret_url = ret_url.strip().lower()
    
    return ret_url

'''
Method to look for text inside balanced quotes to find names
but exclude long exclamations
'''
def parse_balanced_quotes (text):
    ret_quotes = []
    
    bq = re.findall('"([^\\"]+)"', text)
    #is there a better way of removing the punctuation - common theme for project
    bq = str(bq).replace("[", "").replace("u'", "").replace("]", "").replace("'", "").replace('"', "").strip()

    if "," in str(bq):
        for a in str(bq).split(","): 
            if str(a[:1]).isspace():
                str(a).strip() 
            if str(a[:1]) is "u":
                str(a).replace("u", "")
                
            if str(a[:1]).isupper():
                if "!" not in a and len(str(a)) < 40:
                    ret_quotes.append(camel_case(a))  
            else:
                pass     
    else:
        if str(bq[:1]).isspace():
                str(bq[:1]).strip()
        if str(bq[:1]) is "u":
                str(bq[:1]).replace("u", "")
        
        if str(bq[:1]).isupper():
            if  "!" not in bq and len(str(bq)) < 40:
                ret_quotes.append(camel_case(bq))         
        else:
            pass
        
    return ret_quotes

'''
 Method to look for certain patterns in names
 This only works if the name has an honorific. 
 '''
def parseProperNames (text):
    
    ret_name = []
    
    name = re.findall("(?:Mrs)\w{1,3}",text)
    ret_name.append(name)

    name = re.findall("(?:Mr)\w{1,3}",text)
    ret_name.append(name)

    name = re.findall("(?:Ms)\w{1,3}",text)
    ret_name.append(name)
    
    name = re.findall("(?:Miss)\w{1,3}",text)
    ret_name.append(name)

    name = re.findall("(?:Master)\w{1,3}",text)
    ret_name.append(name)

    name = re.findall("(?:Lord)\w{1,3}",text)
    ret_name.append(name)

    name = re.findall("(?:Lady)\w{1,3}",text)
    ret_name.append(name)

        
    return ret_name 

''' 
   Method to return the full author name from db representation 
'''
def author_full (self, author):
        
    full_author = ''
    if "dickens" in author:
        full_author = "Charles Dickens" 
        
    return full_author

'''
   Method to return a geographical place from the header
'''
def find_geographical (text):
    
    place = re.findall(".*\._\s+", text)
    match_place = place
    
    if match_place:
        for m in match_place[0].split("_"):
            place_str = m.strip()
            if place_str[:2].isupper():
                return unicode(camel_case(place_str[0: -1]), 'utf-8')
            else:
                return "No Place"
    else:
        return "No Place"
'''
   Capitalise the first letters and turn the string into camel case to normalise for URIs
'''
def camel_case (text_string):
    return " ".join(t_str.capitalize() for t_str in text_string.split())
    