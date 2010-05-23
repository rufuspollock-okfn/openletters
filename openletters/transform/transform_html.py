from openletters.model import dbase

'''
   Script to output the letters in html
'''

def output_letter (uri):
    
    letter = {}
    
    if uri is None:
        print "uri is empty", uri
    else:
        print "stored uri ", uri
    
    letter_output = ''
    letter_output += "<p>[Sidenote"
    
    letter = dbase.get_letter_text(uri)
    
    for key in letter.iterkeys():
        for n in str(letter[key]).splitlines():
            letter_output += '%s<br />' %(n)
    
    letter_output += '</p>'
    letter_output += '<p><a href="../data/letter_rdf?url='+uri+'">Rdf version</a></p>'
    
    return letter_output

def output_author_index (author):
    authorIndex = ''
    letter = []
    letter = dbase.index_author(author)

    index_items = letter.items()
    index_items.sort()
    
    #TODO: turn author index into a dictionary for other authors
    author_index = ''
    if author == "Dickens":
        author_index = "Charles Dickens"
        
    authorIndex = '<p>An index of letters written by '+author_index+'</p>'
    
    for letter_url, letter_corr in index_items:
        authorIndex += '<p><a href="text?letter=%s">%s</a> written on %s </p>' %(letter_corr[0], letter_corr[1], letter_corr[2])
    
    return authorIndex

