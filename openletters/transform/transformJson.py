import json
from openletters.model import dbase
'''
  Methods for json output
  '''
  
def authorTimeline (author):
    aTimeline = ''
    author = "{'dateTimeFormat:iso8601, events:["
    letters = []
    letters = dbase.createCorrespondents(author)
    print letters
    letter_items = letters.items()
    letter_items.sort()
    
    for count, body in letter_items:
        author += "{"
        author += "type: %s, description, %s, id: %s, title: %s, start: %s" % (author, body[0] , body[1], body[1], body[2])
        author += "}"
        
    author += "]}"
    
    aTimeline = author
    print aTimeline
    return aTimeline