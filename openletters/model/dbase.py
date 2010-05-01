from sqlalchemy import *

from meta import engine as db, metadata
from letter import letter_table
# TODO: remove (backwards compat hack)
users = letter_table


def run(stmt):
    rs = stmt.execute()
    for row in rs:
        #print "row", row
        return row
 
#gets the letter text - where letter_text  
#need to map this to the correct table
def getLetterText(uri): 
    ret_arr = {}
    s = letter_table.select(letter_table.c.perm_url == uri)
    rs = s.execute()
    for row in rs:
        ret_arr[row[0]] = row[6]
    
    return ret_arr

#returns all letters by an author 
def indexAuthor (author):
    ret_index = {}
    index = letter_table.select(letter_table.c.type == author)
    #r =run(index)
    rs = index.execute()
    count = 0
    for row in rs:
        #create dictionary of url and correspondent 
        count += 1
        ret_index[count] = [row[3], row[5], row[7]]
        
    return ret_index

#returns correspondents
def createCorrespondents (author):
    ret_corr = {}
    print "author", author
    index = letter_table.select(letter_table.c.type == author)
    #r =run(index)
    rs = index.execute()
    count = 0
    for row in rs:
        #create dictionary of url and correspondent 
        count += 1
        ret_corr[count] = [row[3], row[5], row[7]]
    print "dbase", ret_corr
    return ret_corr

#gets any annotations for a letter - this will come later
def getAnnotation (url):
    annotation = notes.select(notes.c.url == url)
    r = run(annotation)
    return r

#inserts the annotation - this will come later once the templating as been done
def insertAnnotation (url):
    insertNote = notes.insert(notes.c.url == url)
    r = run(insertNote)
    return r

#void method to insert the data from the parser
#TODO: add in the date to the db  
def insertLetters(url, vol, corr, type, sal, letter, date):
    ins = letter_table.insert()
    db.execute(ins, volume=vol, type=type, perm_url=url, correspondent=corr, salutation=sal, letter_text=letter, letter_date=date)
