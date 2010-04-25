import xml.etree.ElementTree as ET

from openletters.model import data
 
#create an XML of letters for a defined author
def createIndex (author):

    doc = ''
    letterIndex = {}
    letterIndex = data.indexAuthor(author)
    print letterIndex
    root = ET.Element("index")
    #for k,v in letterIndex.items():
    for key in letterIndex.iteritems():
        url = ET.SubElement(root, "url")
        url.text = key
        author = ET.SubElement(url, "author")
        author.text = letterIndex[key[0]]
        date = ET.SubElement(author, "date")
        date.text = letterIndex[key[1]]
        
    doc = ET.ElementTree(root)
    return doc