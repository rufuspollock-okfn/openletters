import xml.etree.ElementTree as ET

class xml_transform:
 
    '''create an XML of letters for a defined author'''
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
            
            if l.letter_text:
                
                l_text = ET.SubElement(letter, "text")
                l_text.text = unicode(self.xml_encode(l.letter_text))
   
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

    def xml_encode (self, text):
        
        return text.replace("&", "&amp;").replace('"', '&quote').replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;")
        