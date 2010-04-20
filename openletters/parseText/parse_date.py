import re
'''
  Gets the relevant line from the letter then breaks it up
  I think that this should be eventually returned as ISO8601 format
'''

def parseDate (letter):
    dateObj = ''
    if "._" in letter:
        dateObj = "dateObj is ", parseLineDate(letter)
        return dateObj

''' 
  Functions finds the year at the moment 
'''
def parseLineDate(obj):
    ret_obj = ''
    h = re.compile(".*(\d{4})")
    mat_m = h.match(obj)
    if mat_m:
        ret_obj = mat_m.group()
        return ret_obj