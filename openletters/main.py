'''
Class to parse the Dickens letters and enter into a store
'''
from parseText import parse_text
from parseText import parse_date

from xml.dom import minidom

from openletters import model

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handle_elements (elementname, element):
    e = element.getElementsByTagName(elementname)
    
    for name in e:
        return handle_parts(elementname, name)

    
def handle_parts (nodename, node):
   # print "<%s>%s</%s>" % (nodename, getText(node.childNodes), nodename)
    return getText(node.childNodes)
    

def load_dickens_letters(fileobj, verbose=True):
    #read = fileobj.read()
    text = minidom.parse(fileobj)

    #split the body into individual letters
    letters  = text.getElementsByTagName('div')
 
    vol = 1
    count = 1
    for letter in letters:
        modelletter = model.Letter(
                    volume=handle_elements("volume", letter), 
                    type=u'dickens',
                    correspondent = handle_elements("correspondent", letter), 
                    salutation=unicode(handle_elements("salutation", letter)),
                    letter_text=unicode(handle_elements("letter", letter)),
                    letter_date=unicode(handle_elements("date", letter))
                    )
        print "date", unicode(handle_elements("date", letter))
        model.Session.add(modelletter)
        model.Session.commit()
    
        if verbose:
            print('Letter %s: \n\t ...' % (count))
            model.Session.remove()
        else:
            print('Letter %s: SKIPPING' % (count))

def load_source (fileobj, verbose=True):
    
    source_text = minidom.parse(fileobj)
    
    letters  = source_text.getElementsByTagName('source')
    title = ''
    for letter in letters:
        modelsource = model.Source (
               source_id=unicode(handle_elements("id", letter)),   
               title=unicode(handle_elements("title", letter)), 
               author=unicode(handle_elements("author", letter)),   
               publn_data=unicode(handle_elements("publication", letter)),
               publn_date=unicode(handle_elements("date", letter)), 
               s_url=unicode(handle_elements("url", letter)),                 
            )
        
        model.Session.add(modelsource)
        model.Session.commit()
    
        if verbose:
            print('Source %s: \n\t ...' % (title))
            model.Session.remove()
        else:
            print('Source : SKIPPING')