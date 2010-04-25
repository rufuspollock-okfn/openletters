import re
'''
  Gets the relevant line from the letter then breaks it up
  I think that this should be eventually returned as ISO8601 format (YYYY-MM-DD)
  as it allows for interoperability and transformation
  TODO: Work on parsing dates like Christmas Eve as 12-24
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
    retObj = ''
    h = re.compile(".*(\d{4})")
    mat_m = h.match(obj)
    if mat_m:
        retObj = mat_m.group()
     
    i = 0
    yr = ''
    mth = ''
    day = ''
    for i in retObj.split():
        
        if (parseYear(i)):
            yr = parseYear(i)
            
        if (parseMonth(i)):
            mth = parseMonth(i)
            
        if (parseDay(i)):
            d = parseDay(i)
            if str(d[0]).isdigit():
                day = d[0]
        
    #padding the dates with 0    
    ret_obj = str(yr).rjust(4,'0')+"-"+str(mth).rjust(2,'0')+"-"+str(day).rjust(2,'0')
    return ret_obj

''' 
  Function finds the year.  
'''   
def parseYear (date):
    yrLine = ''
    yrObj = re.compile("(\d{4})")
    yrMatch = yrObj.match(date)
    if yrMatch:
        yrLine = yrMatch.group()
    
    return yrLine

''' 
  Function finds the month  
'''   
def parseMonth (date):
    mthLine = ''

    month = dict([ ('january',1), ('february',2), ('march',3), ('april',4), ('may',5), ('june',6), ('july',7), ('august',8), ('september',9),
 ('october',10), ('november',11), ('december',12) ])
    
    if str(date).lower() in month:
          mthLine = month[str(date).lower()]
    else:
          mthLine = 00
          
    return mthLine


''' 
  Function finds the day  
  It looks for simple patterns
'''   
def parseDay (date):
    dtLine = ''

    if "nd" in date:
        dtLine = date.split("nd")
    elif "rd" in date:
        dtLine = date.split("rd")
    elif "th" in date:
        dtLine = date.split("th")
    elif "st" in date:
        dtLine = date.split("st")
    
    return dtLine


