import re

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
    ret_url = ret_url.replace(".", "")
    ret_url = ret_url.replace(": ", "")
    if type == "url":
        ret_url = ret_url.replace(" ", "")
        ret_url = ret_url.strip().lower()
    
    return ret_url

'''
Method to look for text inside balanced quotes to find names
but exclude long exclamations
'''
def parseBalancedQuotes (text):
    ret_quotes = []
    

    bq = re.compile("([^\"]+)")
    match_quote = bq.match(text)
    if match_quote:
        m_quote = match_quote.group()
        #trying to make sure that we don't return sentences or exclamations, only titles
        if str(m_quote[1]).isupper() and "!" not in m_quote and len(m_quote) < 41:
            ret_quotes.append(m_quote)
                              
    return ret_quotes

'''
 Method to look for certain patterns in names
 This only works if the name has an honorific. 
 '''
def parseProperNames (text):
    
    ret_name = []
    name = ''
    
    for n in text:
        if "Mrs" in n:
            if (n+1).isupper and (n+2).isupper and (n+3):
                name = n + (n+1) + (n+2) + (n+3)
                ret_name.append(name)
            elif (n+1).isupper and (n+2).isupper:
                name = n + (n+1) + (n+2)
                ret_name.append(name)
            
        if "Mr" in n:
            if (n+1).isupper and (n+2).isupper and (n+3):
                name = n + (n+1) + (n+2) + (n+3)
                ret_name.append(name)
            elif (n+1).isupper and (n+2).isupper:
                name = n + (n+1) + (n+2)
                ret_name.append(name)
        
        if "Miss" in n:
            if (n+1).isupper and (n+2).isupper and (n+3):
                name = n + (n+1) + (n+2) + (n+3)
                ret_name.append(name)
            elif (n+1).isupper and (n+2).isupper:
                name = n + (n+1) + (n+2)
                ret_name.append(name)
        
        if "Ms" in n:
            if (n+1).isupper and (n+2).isupper and (n+3):
                name = n + (n+1) + (n+2) + (n+3)
                ret_name.append(name)
            elif (n+1).isupper and (n+2).isupper:
                name = n + (n+1) + (n+2)
                ret_name.append(name)
        
        if "Master" in n:
            if (n+1).isupper and (n+2).isupper and (n+3):
                name = n + (n+1) + (n+2) + (n+3)
                ret_name.append(name)
            elif (n+1).isupper and (n+2).isupper:
                name = n + (n+1) + (n+2)
                ret_name.append(name)
                
        if "Lady" in n:
            if (n+1).isupper and (n+2).isupper and (n+3):
                name = n + (n+1) + (n+2) + (n+3)
                ret_name.append(name)
            elif (n+1).isupper and (n+2).isupper:
                name = n + (n+1) + (n+2)
                ret_name.append(name)
        
    return ret_name 