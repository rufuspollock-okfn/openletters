from sqlalchemy import *

#TODO: change this run off the .ini file. 
db = create_engine('engine://user:pwrd@host/db')


#for testing echo out the SQL
db.echo = False

metadata = MetaData(db)

#define the table mappings here
users = Table('text', metadata, autoload=True)
notes = Table('annotation', metadata, autoload=True)


def run(stmt):
    rs = stmt.execute()
    for row in rs:
        #print "row", row
        return row
 
#gets the letter text - where letter_text       
def getLetterText(uri): 
    s = users.select(users.c.perm_url == uri)
    r = run(s)
    return r

#returns all letters by an author 
def indexAuthor (author):
    ret_index = {}
    index = users.select(users.c.type == author)
    #r =run(index)
    rs = index.execute()
    for row in rs:
        #create dictionary of url and correspondent 
        ret_index[row[3]] = row[4]
    return ret_index

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
