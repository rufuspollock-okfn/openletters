import json
from openletters.model import dbase
'''
  Methods for json output
  '''
  
def author_timeline (author):
    a_timeline = ''
    author_index = "{'dateTimeFormat:iso8601, events:["
    letters = []
    letters = dbase.create_correspondents(author)
    letter_items = letters.items()
    letter_items.sort()
    
    for count, body in letter_items:
        author_index += "{"
        author_index += "type: %s, description: %s, id: %s, title: %s, start: %s" % (author, author_timeline_letter(str(body[3]), str(body[1]), str(body[2])) , body[1], body[1], body[2])
        author_index += "}"
        
    author_index += "]}"
    
    a_timeline = json.dumps(author_index, sort_keys=True, indent=4)

    return a_timeline

def author_timeline_letter (id, correspondent, time):
    
    a_letter_text = ''
    
    a_letter_text = "Letter written to " + correspondent + " on " + time + "."
    a_letter_text +=  'The text can be viewed at <a href="http://www.opencorrespondence.org/letters/view/'+id+'">http://www.opencorrespondence.org/letters/view/'+id+'</a>'
    
    return a_letter_text