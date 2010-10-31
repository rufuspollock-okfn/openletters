import xml.etree.ElementTree as ET
import urllib

from openletters.model import dbase

class xml_transform:
 
    '''create XML of letters for a defined author'''
    def index_xml (self, letters):
    
        root = ET.Element("opencorrespondence")
        
        
        for l in letters:
            letter = ET.SubElement(root, "letter")
            url = ET.SubElement(letter, "author")
            url.text = unicode(l.type)
            author = ET.SubElement(letter, "correspondent")
            author.text = unicode(l.correspondent)
            date = ET.SubElement(letter, "date")
            date.text = unicode(l.letter_date)
            id = ET.SubElement(letter, "id")
            id.text = unicode(str(l.id))
            
            #if l.letter_text:
            #    
            #    l_text = ET.SubElement(letter, "text")
            #    l_text.text = unicode(self.xml_encode(l.letter_text))
   
        doc = ET.tostring(root, "UTF-8")
    
        return doc
    
    def letter_xml (self, letters):
            
        root = ET.Element("opencorrespondence")
        
        
        for l in letters:
            letter = ET.SubElement(root, "letter")
            url = ET.SubElement(letter, "author")
            url.text = unicode(l.type)
            date = ET.SubElement(letter, "date")
            date.text = unicode(l.letter_date)
            author = ET.SubElement(letter, "correspondent")
            author.text = unicode(l.correspondent)
            l_text = ET.SubElement(letter, "letter_text")
            l_text.text = unicode(l.letter_text)

            
            if l.letter_text:
                
                l_text = ET.SubElement(letter, "text")
                l_text.text = unicode(self.xml_encode(l.letter_text))
   
        doc = ET.tostring(root, "UTF-8")
    
        return doc
    
    def corres_xml (self, corr, letters):
        
        root = ET.Element("opencorrespondence")
        
        letter = ET.SubElement(root, "person")
        author = ET.SubElement(letter, "correspondent")
        author.text = unicode(corr)
        
        for name, url in letters:
 
            nick = ET.SubElement(letter, "nick")
            nick.text = unicode(name)

   
        doc = ET.tostring(root, "UTF-8")
        
        return doc
    
    '''
        Function to create xml for Simile timeline
    '''
    def endpoint_xml (self, type = ''):
        
        root = ET.Element("data", {'date-time-format': 'ISO 8601'})
        
        letter = {}  
        letter = dbase.get_endpoint_rdf()
    
        letter_items = letter.items()
        letter_items.sort()
          
        for url, utext in letter_items:
            if type == "simile":
                event = ET.SubElement(root, "event", {"start": str(utext[3])+'T00:00:00Z', "title": utext[1] , "link": 'http://www.opencorrespondence.org/letters/view/dickens/' + urllib.quote(utext[1]) + '/' + str(url)  })
                event.text = unicode("Letter to " + utext[1])
            else:
                letter = ET.SubElement(root, "letter")
                aurl = ET.SubElement(letter, "author")
                aurl.text = unicode("Charles Dickens")
                author = ET.SubElement(letter, "correspondent")
                author.text = unicode(utext[1])
                date = ET.SubElement(letter, "date")
                date.text = unicode(utext[3])
                id = ET.SubElement(letter, "id")
                id.text = unicode('http://www.opencorrespondence.org/letters/view/dickens/' + urllib.quote(utext[1]) + '/' + str(url))
        
        doc  = ET.tostring(root, "UTF-8")
        return doc

    def xml_encode (self, text):
        
        return text.replace("&", "&amp;").replace('"', '&quote').replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;")
        