
'''
Class to parse the Dickens letters and enter into a store
'''
import unicodedata, urllib, os, xapian

from pylons import request, response, session, tmpl_context as c, config

from ofs.local import OFS

from xml.dom import minidom

from openletters.parse import parse_text, parse_date
from openletters import model

from openletters.transform.transform_rdf import rdf_transform
from openletters.transform.transform_json import json_transform
from openletters.transform.transform_xml import xml_transform

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(unicodedata.normalize('NFKC', node.data))
    return ''.join(rc)

def handle_elements (elementname, element):
    e = element.getElementsByTagName(elementname)
    
    for name in e:
        return handle_parts(elementname, name)

    
def handle_parts (nodename, node):
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
                    letter_date=unicode(handle_elements("date", letter)),
                    letter_place=unicode(handle_elements("place", letter))
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
            
def load_texts (fileobj, verbose=True):
    
    source_text = minidom.parse(fileobj)
    
    letters  = source_text.getElementsByTagName('book')
    book_title = ''
    for letter in letters:
        modelbook = model.Book (
               book_id=unicode(handle_elements("id", letter)),   
               book_title=unicode(handle_elements("title", letter)),
               book_pub=unicode(handle_elements("mag_start", letter)),
               book_end_pub=unicode(handle_elements("mag_end", letter)),  
               aka=unicode(handle_elements("aka", letter)),
               aka2=unicode(handle_elements("aka2", letter)),
               description=unicode(handle_elements("description", letter)),
               url=unicode(handle_elements("url", letter)),
               source=unicode(handle_elements("source", letter)),
            )
        
        model.Session.add(modelbook)
        model.Session.commit()
    
        if verbose:
            print('Text %s: \n\t ...' % (book_title))
            model.Session.remove()
        else:
            print('Source : SKIPPING')

def load_locations (fileobj, verbose=True):
    
    source_text = minidom.parse(fileobj)
    
    letters  = source_text.getElementsByTagName('location')
    place = ''
    for letter in letters:
        modellocation = model.Location (
               placeid=unicode(handle_elements("place", letter)),   
               latitude=unicode(handle_elements("lat", letter)),
               longitude=unicode(handle_elements("lon", letter)),
               url=unicode(handle_elements("url", letter)),
               source=unicode(handle_elements("source", letter)),
            )
        
        model.Session.add(modellocation)
        model.Session.commit()
    
        if verbose:
            print('Location %s: \n\t ...' % (place))
            model.Session.remove()
        else:
            print('Location : SKIPPING')
            

def index_letters(self, type, fileobj):

    #open a writable database on the xapian-tcpsrvr
    try :
        database = xapian.WritableDatabase(config['xapian_host'], xapian.DB_CREATE_OR_OPEN)
    except xapian.DatabaseOpeningError:
        return 'Cannot open database for Xapian'

    indexer = xapian.TermGenerator()
    indexer.set_stemmer(xapian.Stem('english'))
    
    xapian_file_name = 0
    count = 0
    text = minidom.parse(fileobj)
    #split the body into individual letters
    letters  = text.getElementsByTagName('div')
    #open the XML, parse the letter id
    for letter in letters:
        count +=1
        text=unicode(handle_elements("letter", letter))
        corr=unicode(handle_elements("correspondent", letter))
            
        document = xapian.Document()
        document.set_data(text)
        
        letter_index = type + "/" + urllib.quote(corr) + "/" + str(count)

        print "indexing %s" ,letter_index
        document.add_value(xapian_file_name, letter_index)
        
        indexer.set_document(document)
        indexer.index_text(text)
        database.add_document(document)
        
    database.flush()
    
def create_endpoint ():
    #delete any existing endpoints first before loading
    o = OFS()
    
    end = o.claim_bucket('end')
    
    for b in o.list_buckets():
        if o.exists(b, "rdfendpoint"): o.del_stream(b, "rdfendpoint")
        #else: rdf_id = o.claim_bucket('rdfendpoint')
        if o.exists(b, "jsonendpoint"): o.del_stream(b, "jsonendpoint")
        #else: js_store = o.claim_bucket('jsonendpoint')
        if o.exists(b, "xmlendpoint"): o.del_stream(b, "xmlendpoint")
        #else: xm_data = o.claim_bucket('xmlendpoint')
        if o.exists(b, "simileend"): o.del_stream(b, "simileend")
        #else: sim_data = o.claim_bucket('simileend')
        if o.exists(b, "locationdata"): o.del_stream(b, "location")

    rdf = rdf_transform()
    rdf_data = rdf.create_rdf_end()
    o.put_stream(end, 'endpoint', rdf_data)
    
    json = json_transform()
    json_data = json.to_end_dict()
    o.put_stream(end, 'jsonendpoint', json_data)
    
    xml = xml_transform()
    x_data = xml.endpoint_xml()
    o.put_stream(end, 'xmlendpoint', x_data)  
    
    xml_data = xml.endpoint_xml("simile")
    o.put_stream(end, 'simileend', xml_data)
        
    
def __store (self, ofsobject, data_store, data_name):
    
    store_id = ofsobject.claim_bucket(data_name)
    ofsobject.put_stream(store_id, data_name, data_store)
