from parseText import parse_text
from parseText import parse_date

'''
Class to parse the Dickens letters and enter into a store
'''

text = open('doc/letterone.txt').read()

#remove the asterisks
text = text.replace("*","")

#split the body into individual letters
for letter in text.split("[Sidenote"):
    m_let = parse_text.parseCorrespondent(letter)
    #print m_let
    for l in letter.split("\n"):
        #print "line is", line
        m_sal = parse_text.parseSalutation(l)
        if m_sal != '':
            '''need to put the line into a list/dictionary'''
            print m_sal
        m_date_let = parse_date.parseDate(l)
        print m_date_let