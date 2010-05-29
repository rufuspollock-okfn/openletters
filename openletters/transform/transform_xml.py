import xml.etree.ElementTree as ET

from openletters.model import dbase
 
#create an XML of letters for a defined author
def createIndex (author):

    doc = ''
    letter = []
    #letterIndexUrl, letterIndexCorr, letterIndexDt = data.indexAuthor(author)
    letter = dbase.index_author(author)

    root = ET.Element("index")

    index_items = letter.items()
    index_items.sort()
    
    url = ET.SubElement(root, "url")
    author = ET.SubElement(url, "correspondent")
    date = ET.SubElement(author, "date")
    doc = '<?xml version="1.0" encoding="ISO-8859-1"?>'
    doc += "<index>"
    for letter_url, letter_corr in index_items:
        doc += "<letter>"
        doc += "<url>http://www.opencorrespondence.org/letter/view/%s</url><corr>%s</corr><date>%s</date>" %(letter_corr[0], letter_corr[1],letter_corr[2])
        doc += "</letter>"
    #for key in letter.iteritems():
    #for n in letter:
        #url.text = letter_corr[0]
        #author.text = letter_corr[1]
        #date.text = letter_corr[2]
    doc += "</index>"   
    

    return doc