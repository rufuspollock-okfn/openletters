from openletters.model import data

'''
   Script to output the letters in html
'''

def outputLetter (uri):
    letter = {}
    letter = data.getLetterText(uri)
    letter_output = '<p>'

    letter_output = "[Sidenote"
    for key in letter.iterkeys():
        for n in str(letter[key]).splitlines():
            letter_output += '%s<br />' %(n)
    
    letter_output += '</p>'
    
    return letter_output