import xml.etree.ElementTree as ET
import urllib

from openletters.model import dbase

from openletters.parse import parse_text

class xml_transform:
 
    
    def index_xml (self, letters):
        print "inside xml"
        '''create XML of letters for a defined author'''
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
        ''' 
            Function to return XML
        '''
        
        root = ET.Element("tei")
        root.set('xmlns', 'http://www.tei-c.org/ns/1.0')
        
        teiHeader = ET.SubElement(root, "teiHeader")
        fileDesc = ET.SubElement(teiHeader, "fileDesc")
                
        titleStmt = ET.SubElement(fileDesc, "titleStmt")
        title = ET.SubElement(titleStmt, "title")
        title.text = u"Letter from Charles Dickens"
        author = ET.SubElement(titleStmt, "author")
        author.text = u"Charles Dickens"
        editor = ET.SubElement(titleStmt, "editor")
        editor.text = u"Open Correspondence project"
                      
        respStmt = ET.SubElement(titleStmt, "respStmt")
        resp = ET.SubElement(respStmt, "resp")
        resp.text = u"Conversion to TEI-conformant XML"
        name = ET.SubElement(respStmt, "name")
        name.text = u"The Open Knowledge Foundation" 
        extent = ET.SubElement(titleStmt,"extent")
        extent.text = u"Less than 1Mb"
        
        #sourceDesc element        
        sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
        p = ET.SubElement(sourceDesc, "p")
        p.text = u"Digitised from Gutenberg source"
        bibFull = ET.SubElement(sourceDesc, "bibl")
        pub_title = ET.SubElement(bibFull, "title")
        pub_title.text = u"The Letter of Charles Dickens"
        pub_author = ET.SubElement(bibFull, "author")
        pub_author.text = u"Charles Dickens"
        pub_ed = ET.SubElement(bibFull, "editor")
        pub_ed.text = u"Mamie Dickens and Georgina Hogarth"
        publisher = ET.SubElement(bibFull, "publisher")
        publisher.text = u"Chapman and Hall"
        pubPlace = ET.SubElement(bibFull, "pubPlace")
        pubPlace.text = u"London"
        pubDate = ET.SubElement(bibFull, "date")
        pubDate.text = "1870"

        #encoding description
        encode_stmt = ET.SubElement(fileDesc, "encodingDesc")
        project_desc = ET.SubElement(encode_stmt, "projectDesc")
        project_desc.text = u"Open Correspondence is a project to mine the social network of Nineteenth century letters. As part of the project it aims to provide the letters in various forms such as XML, JSON and RDF"
        editorial_decl = ET.SubElement(encode_stmt, "editorialDecl")
        editorial_decl.text = u"Some diphthongs (such  as 'ae') have been modernised."
        sampling_decl = ET.SubElement(encode_stmt, "samplingDecl")
        sampling_decl.text = u"An attempt has been made to encode the letters as they are in the original file. Work still needs to be done on the annotations."
        
        #edition statement - made about this edition
        edPubStmt = ET.SubElement(fileDesc, "publicationStmt")
        edPub = ET.SubElement(edPubStmt, "distributor")
        edPub.text = u"Open Correspondence project for The Open Knowledge Foundation"
        edAddr = ET.SubElement(edPubStmt, "address")
        edPubPlace = ET.SubElement(edAddr, "addrLine")
        edPubPlace.text = u"www.opencorrespondence.org"
        edPubDate = ET.SubElement(edPubStmt, "date")
        edPubDate.text = "2011"
        
        avail = ET.SubElement(edPubStmt, "availability")
        avail.text = u"This text is available under an Open Data licence (www.opendefinition.org)"
        
        letText = ET.SubElement(root, "text")
        
        letBody = ET.SubElement(letText, "body")
        
        for l in letters:
            letSeg = ET.SubElement(letText, "seg")
            letFigEnt = ET.SubElement(letSeg, "figure_entity")
            letFigEnt.text = unicode(str(l.id))
            letFigDesc = ET.SubElement(letSeg, "figureDesc")
            
            div = ET.SubElement(letBody, "div", type="letter")
            
            letHead = ET.SubElement(div, "head")
            letHeadName = ET.SubElement(letHead, "name", name=unicode(l.correspondent))
            letHeadDate = ET.SubElement(letHead, "date", date= unicode(l.letter_date))
            letHeadDate.text = unicode(l.letter_date)
            
            letOpen = ET.SubElement(letBody, "opener")
            lines = 0
            sal = ''
            dtLn = ''
            for let in l.letter_text.splitlines():
                lines += 1
                m = parse_text.parse_salutation_line(let)
                if m != '': sal = m
                
                if "._" in let:  dtLn = let
                     
                
            letAddr = ET.SubElement(letOpen, "dateLine")
            letAddr.text = dtLn
            letSalute = ET.SubElement(letOpen, "salutation")
            letSalute.text = sal
            
            letText = ET.SubElement(letBody, "text")
            letText.text = unicode(l.letter_text)
            
            letClose = ET.SubElement(letBody, "closer")
            letSigned = ET.SubElement(letClose, "signature")
            letSigned.text = unicode(l.type)
            
        doc = ET.tostring(root, "UTF-8")
    
        return doc
    
    def corres_xml (self, corr, letters):
        ''' 
           Function to return a correspondent in XML
        '''
        root = ET.Element("opencorrespondence")
        
        letter = ET.SubElement(root, "person")
        author = ET.SubElement(letter, "correspondent")
        author.text = unicode(corr)
        
        for name, url in letters:
            nick = ET.SubElement(letter, "nick")
            nick.text = unicode(name)

        doc = ET.tostring(root, "UTF-8")
        
        return doc
    
    def endpoint_xml (self, type = ''):
        '''
            Function to create xml for Simile timeline and xml endpoint
        '''
        if type =="simile":
            root = ET.Element("data", {'date-time-format': 'ISO 8601'})
        else:
            root = ET.Element("tei")
        
            teiHeader = ET.SubElement(root, "teiHeader")
            fileDesc = ET.SubElement(teiHeader, "fileDesc")
                    
            titleStmt = ET.SubElement(fileDesc, "titleStmt")
            title = ET.SubElement(titleStmt, "title")
            title.text = u"Letter from Charles Dickens"
            author = ET.SubElement(titleStmt, "author")
            author.text = u"Charles Dickens"
            editor = ET.SubElement(titleStmt, "editor")
            editor.text = u"Open Correspondence project"
                          
            respStmt = ET.SubElement(titleStmt, "respStmt")
            resp = ET.SubElement(respStmt, "resp")
            resp.text = u"Conversion to TEI-conformant XML"
            name = ET.SubElement(respStmt, "name")
            name.text = u"The Open Knowledge Foundation" 
            extent = ET.SubElement(titleStmt,"extent")
            extent.text = u"Less than 1Mb"
            
            #sourceDesc element        
            sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
            p = ET.SubElement(sourceDesc, "p")
            p.text = u"Digitised from Gutenberg source"
            bibFull = ET.SubElement(sourceDesc, "bibl")
            pub_title = ET.SubElement(bibFull, "title")
            pub_title.text = u"The Letter of Charles Dickens"
            pub_author = ET.SubElement(bibFull, "author")
            pub_author.text = u"Charles Dickens"
            pub_ed = ET.SubElement(bibFull, "editor")
            pub_ed.text = u"Mamie Dickens and Georgina Hogarth"
            publisher = ET.SubElement(bibFull, "publisher")
            publisher.text = u"Chapman and Hall"
            pubPlace = ET.SubElement(bibFull, "pubPlace")
            pubPlace.text = u"London"
            pubDate = ET.SubElement(bibFull, "date")
            pubDate.text = "1870"
    
            #encoding description
            encode_stmt = ET.SubElement(fileDesc, "encodingDesc")
            project_desc = ET.SubElement(encode_stmt, "projectDesc")
            project_desc.text = u"Open Correspondence is a project to mine the social network of Nineteenth century letters. As part of the project it aims to provide the letters in various forms such as XML, JSON and RDF"
            editorial_decl = ET.SubElement(encode_stmt, "editorialDecl")
            editorial_decl.text = u"Some diphthongs (such  as 'ae') have been modernised."
            sampling_decl = ET.SubElement(encode_stmt, "samplingDecl")
            sampling_decl.text = u"An attempt has been made to encode the letters as they are in the original file. Work still needs to be done on the annotations."
            
            #edition statement - made about this edition
            edPubStmt = ET.SubElement(fileDesc, "publicationStmt")
            edPub = ET.SubElement(edPubStmt, "distributor")
            edPub.text = u"Open Correspondence project for The Open Knowledge Foundation"
            edAddr = ET.SubElement(edPubStmt, "address")
            edPubPlace = ET.SubElement(edAddr, "addrLine")
            edPubPlace.text = u"www.opencorrespondence.org"
            edPubDate = ET.SubElement(edPubStmt, "date")
            edPubDate.text = "2011"
            
            avail = ET.SubElement(edPubStmt, "availability")
            avail.text = u"This text is available under an Open Data licence (www.opendefinition.org)"
            
            letText = ET.SubElement(root, "text")
            
            letBody = ET.SubElement(letText, "body")
        
        letter = {}  
        letter = dbase.get_endpoint_rdf()
    
        letter_items = letter.items()
        letter_items.sort()
          
        for url, utext in letter_items:
            if type == "simile":
                event = ET.SubElement(root, "event", {"start": str(utext[3])+'T00:00:00Z', "title": str(utext[1]) , "link": 'http://www.opencorrespondence.org/letters/view/dickens/' + urllib.quote(str(utext[1])) + '/' + str(url)  })
                event.text = unicode("Letter to " + str(utext[1]))
            else:
                #letter = ET.SubElement(root, "letter")
                #aurl = ET.SubElement(letter, "author")
                #aurl.text = unicode("Charles Dickens")
                #author = ET.SubElement(letter, "correspondent")
                #author.text = unicode(utext[1])
                #date = ET.SubElement(letter, "date")
                #date.text = unicode(utext[3])
                #id = ET.SubElement(letter, "id")
                #id.text = unicode('http://www.opencorrespondence.org/letters/view/dickens/' + urllib.quote(str(utext[1])) + '/' + str(url))
                
                letSeg = ET.SubElement(letText, "seg")
                letFigEnt = ET.SubElement(letSeg, "figure_entity")
                letFigEnt.text = unicode(str('http://www.opencorrespondence.org/letters/view/dickens/' + urllib.quote(str(utext[1])) + '/' + str(url)))
                letFigDesc = ET.SubElement(letSeg, "figureDesc")
                
                div = ET.SubElement(letBody, "div", type="letter")
                
                letHead = ET.SubElement(div, "head")
                letHeadName = ET.SubElement(letHead, "name", name=unicode(str(utext[1])))
                #letHeadDate = ET.SubElement(letHead, "date", date= unicode(l.letter_date))
                #letHeadDate.text = unicode(utext[2])
                
                letOpen = ET.SubElement(div, "opener")
                lines = 0
                sal = ''
                dtLn = ''
                #for let in str(utext[2]).splitlines():
                #    lines += 1
                #    m = parse_text.parse_salutation_line(utext[2])
                #    if m != '': sal = m
                #    
                #    if "._" in let:  dtLn = let
                         
                    
                letAddr = ET.SubElement(letOpen, "dateLine")
                letAddr.text = unicode(str(utext[3]))
                letSalute = ET.SubElement(letOpen, "salutation")
                letSalute.text = sal
                
                letText = ET.SubElement(div, "text")
                letText.text = unicode(utext[2])
                
                letClose = ET.SubElement(div, "closer")
                letSigned = ET.SubElement(letClose, "signature")
                letSigned.text = unicode("Charles Dickens")
        
        
        doc  = ET.tostring(root, "UTF-8")
        return doc
    
    def create_place (self, placeobj):
        
        root = ET.Element("opencorrespondence")
        for location in placeobj:
            place = ET.SubElement(root, "placename", location.placeid)
            lat = ET.SubElement(place, "latitude")
            lat.text = location.latitude
            long = ET.SubElement(place, "longitude")
            long.text = location.longitude
            id = ET.SubElement(place, "source")
            id.text = unicode(location.source)
            
        doc  = ET.tostring(root, "UTF-8")
        
        return doc

    def xml_encode (self, text):
        
        return text.replace("&", "&amp;").replace('"', '&quote').replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;")
        