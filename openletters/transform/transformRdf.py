import re
import rdflib

from openletters.model import dbase
''' 
   rdf related scripts for open letters
'''

'''
  creates an rdf representation of letter
  @param uri 
  @return letter_rdf
  '''
def createRdfLetter (uri):
    
    letter_rdf = ''
    
    letter = dbase.getLetterText(uri)
    
    
    return letter_rdf