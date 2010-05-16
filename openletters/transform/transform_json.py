import json
from openletters.model import dbase
'''
  Methods for json output
  '''
  
def author_timeline (author):
    a_timeline = ''
    author_index = "{'dateTimeFormat:iso8601, events:["
    letters = []
    letters = dbase.createCorrespondents(author)
    print letters
    letter_items = letters.items()
    letter_items.sort()
    
    for count, body in letter_items:
        author_index += "{"
        author_index += "type: %s, description: %s, id: %s, title: %s, start: %s" % (author, body[0] , body[1], body[1], body[2])
        author_index += "}"
        
    author_index += "]}"
    
    a_timeline = json.dumps(author_index, sort_keys=True, indent=4)

    return a_timeline