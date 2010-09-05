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
    m_quote = ''
    bq = re.findall('"([^\\"]+)"', text)
    bq = str(bq).replace("[", "").replace("u'", "").replace("]", "").replace("'", "").strip()

    if "," in str(bq):
        for a in str(bq).split(","): 
            if str(a[0:1]).isspace():
                str(a).strip() 
            if str(a[0:1]) is "u":
                str(a).replace("u", "")

            if str(a[0:1]).isupper() and "!" not in a and len(str(a)) < 40:
                ret_quotes.append(a)  
            else:
                pass     
    else:
        if str(bq[0:1]).isspace():
                str(bq[0:1]).strip()
        if str(bq[0:1]) is "u":
                str(bq[0:1]).replace("u", "")
                           
        if str(bq[0:1]).isupper and "!" not in bq and len(str(bq)) < 40:
            ret_quotes.append(bq)         
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