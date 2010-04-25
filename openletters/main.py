from parseText import parse_text
from parseText import parse_date

from model import data

'''
Class to parse the Dickens letters and enter into a store
'''

text = open('./docs/letter.txt').read()

#remove the asterisks
text = text.replace("*","")

#split the body into individual letters
count = 0
for letter in text.split("[Sidenote"):
    m_sal = ''
    m_date_let = ''
    
    m_let = parse_text.stripPunc(parse_text.parseCorrespondent(letter), '')
    count += 1
    
    m_url = str(count) + str(parse_text.stripPunc(m_let, "url"))
    #print m_let
    for l in letter.split("\n"):
        m = parse_text.parseSalutation(l)
        if m != '':
            m_sal = m[1]
        
        
        if "._" in l:
            if "_" in l:
                 n = l.split("_")
                 m_date_let = parse_date.parseDate(n[1])
                 
    if m_url != "1none":
        data.insertLetters(m_url, 1, m_let, 'dickens', m_sal, letter, m_date_let)

    