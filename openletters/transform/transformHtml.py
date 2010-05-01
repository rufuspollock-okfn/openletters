from openletters.model import dbase

'''
   Script to output the letters in html
'''

def outputLetter (uri):
    letter = {}
    letter = dbase.getLetterText(uri)
    letter_output = '<p>'

    letter_output = "[Sidenote"
    for key in letter.iterkeys():
        for n in str(letter[key]).splitlines():
            letter_output += '%s<br />' %(n)
    
    letter_output += '</p>'
    
    return letter_output

def outputAuthorIndex (author):
    authorIndex = ''
    letter = []
    letter = dbase.indexAuthor(author)

    index_items = letter.items()
    index_items.sort()
    
    for letter_url, letter_corr in index_items:
        authorIndex += '<p><a href="letter?letter=%s">%s</a> written on %s </p>' %(letter_corr[0], letter_corr[1], letter_corr[2])
    
    return authorIndex
    