import re

'''
   Parsing methods
   @author: Iain Emsley (print.crimes@yatterings.com)
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
    if type == "url":
        ret_url = ret_url.replace(" ", "")
        ret_url = ret_url.replace(":", "")
        ret_url = ret_url.strip().lower()
    
    return ret_url