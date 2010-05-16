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

def output_schema():
    
    schema_text = ''
    
    schema_text += '<p>The Open Correspondence project re-uses schemas where possible.</p>'
    schema_text += '<p>It uses <a href="http://purl.org/dc/elements/1.1/">Dublin Core</a>,'
    schema_text += ' <a href="http://xmlns.com/foaf/0.1/">Friend of a Friend</a> and <a href="http://www.isi.edu/~pan/damltime/time-entry.owl#">OWL time</a>.'
    schema_text += 'There are sections of the letter that these schemas do not cover.'
    schema_text += 'The letter schema is designed to patch these holes to allow users to link letters and the letter texts. </p>'
    
    schema_text += '<h4>Letter schema</h4>'
    
    schema_text += '<p>Namespace: http://purl.org/letter</p>'
    
    schema_text += '<h6>Character</h6>'
    schema_text += '<p>A fictional person who is referenced in the text. This element is used to disambiguated between fictional and non-fictional characters. Non-fictional, i.e. real people, are denoted by foaf:Person. Character is a subset of foaf:Person and is intended for fictional people. For example, in a letter from an author to an agent, the author may describing their latest project.</p>'
    
    schema_text += '<h6>Correspondent</h6>'
    schema_text += '<p>This field denotes the correspondent of the letter.  It is a subset of foaf:Person as it should denote a real person. (However it is perfectly possible for a fictional letter to be written and in this case it would perhaps be inappropriate to use foaf:Person).<br />'
    schema_text += 'foaf:nick can be used to highlight the different ways that the correspondent is addressed by the author.</p>'
    
    schema_text += '<h6>personReferred</h6>'
    schema_text += '<p>This field refers to a person who is referred to in the body of the letter</p>'
    
    schema_text += '<h6>textReferred</h6>'
    schema_text += '<p>This refers to a text (book, verse or similar) which is referred to in the letter being serialised. It is intended to allow the building of graphs between the letters where a text is being referred to so that a graph can be built of what an author was doing or thinking about a text around the time or after writing the text. It is designed to allow for some contextualisation of the referred work. It could also be used to build a reading list, possible influences or forgotten works that the author was aware of at the time.</p>'

    
    return schema_text
    