import re
'''
  Gets the relevant line from the letter then breaks it up
'''

def parseDate (letter):
    dateObj = ''
    #dateObj = re.findall("_", letter)
    #date = re.compile("(?<=_).*")
    #lett_date = date.match(letter)
    #if lett_date:
    #    dateObj = lett_date.group()
    if "_" in letter:
        dateObj = "dateObj is ", parseLineDate(letter)
        return dateObj
    
def parseLineDate(obj):
    ret_obj = ''
    h = re.compile("(\d+{4})", obj)
    mat_m = h.match(obj)
    if mat_m:
        ret_obj = mat_m
        return ret_obj