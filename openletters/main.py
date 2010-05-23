'''
Class to parse the Dickens letters and enter into a store
'''
from parseText import parse_text
from parseText import parse_date

from openletters import model

def load_dickens_letters(fileobj, verbose=True):
    text = fileobj.read()
    #remove the asterisks
    text = text.replace("*","")

    #split the body into individual letters
    count = 0
    for letter in text.split("[Sidenote"):
        m_sal = u''
        m_date_let = u''
        m_let = unicode(parse_text.stripPunc(
            parse_text.parseCorrespondent(letter),
            ''))
        m_url = unicode(count) + unicode(parse_text.stripPunc(m_let, "url"))
        count += 1
        
        #print m_let
        for l in letter.split("\n"):
            m = parse_text.parseSalutation(l)
            if m != '':
                m_sal = m[1]
            
            if "._" in l:
                if "_" in l:
                     n = l.split("_")
                     m_date_let = unicode(parse_date.parseDate(n[1]))
                     
        if m_url != "1none":
            vol = 1
            modelletter = model.Letter(volume=vol, type=u'dickens', perm_url=m_url,
                    correspondent=m_let, salutation=unicode(m_sal),
                    letter_text=unicode(letter),
                    letter_date=m_date_let)
            model.Session.add(modelletter)
            model.Session.commit()
            if verbose:
                print('Letter %s: %s\n\t%s ...' % (count, m_let, letter[:15]))
            model.Session.remove()
        else:
            print('Letter %s: SKIPPING' % (count))
        
