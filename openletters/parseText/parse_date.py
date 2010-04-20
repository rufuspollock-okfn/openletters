import re
'''
  Gets the relevant line from the letter then breaks it up
  I think that this should be eventually returned as ISO8601 format (YYYY-MM-DD)
  as it allows for interoperability and transformation
'''

def parseDate (letter):
    dateObj = ''
    dateObj = parseLineDate(letter)
    return dateObj

''' 
  Function finds the line with the year
'''
def parseLineDate(obj):
    ret_obj = ''
    h = re.compile(".*(\d{4})")
    mat_m = h.match(obj)
    if mat_m:
        ret_obj = mat_m.group()
        return ret_obj

''' 
  Function finds the year.  
'''   
def parseYear (date):
    yrLine = ''
    
    
    return yrLine

''' 
  Function finds the month  
'''   
def parseMonth (date):
    mthLine = ''
    
    
    return mthLine


''' 
  Function finds the day  
'''   
def parseDat (date):
    dtLine = ''
    
    
    return dtLine
