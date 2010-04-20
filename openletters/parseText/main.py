import parse_text
import parse_date

'''
Class to parse the Dickens letters and enter into a store
'''

text = open('../docs/letterone.txt').read()

#remove the asterisks
text = text.replace("*","")

#split the body into individual letters
count = 0
for letter in text.split("[Sidenote"):
    m_sal = ''
    m_let = parse_text.stripPunc(parse_text.parseCorrespondent(letter), '')
    count += 1
    
    m_url = str(count) + str(parse_text.stripPunc(m_let, "url"))
    #print m_let
    for l in letter.split("\n"):
        m = parse_text.parseSalutation(l)
        if m != '':
            m_sal = m[1]
        
        #if "._" in l:
        m_date_let = parse_date.parseDate(l)
        if m_date_let != '':
            print "date",  m_date_let
    #insertLetters(m_url, 1, m_let, m_sal, letter)
    print "url", m_url
    print "corres", m_let
    print "sal", m_sal
    #print "letter", letter
    