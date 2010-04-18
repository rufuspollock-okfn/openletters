from sqlalchemy import *

#TODO: change this run off the .ini file. 
db = create_engine('engine://user:pwrd@host/db')


#for testing echo out the SQL
db.echo = True

metadata = MetaData(db)

#define the table mappings here
users = Table('text', metadata, autoload=True)
notes = Table('annotation', metadata, autoload=True)
tags = Table('tags', metadata, autoload=True)

def run(stmt):
    rs = stmt.execute()
    for row in rs:
        #print "row", row
        return row
 
#gets the letter text - where letter_text       
def getLetterText(self,uri): 
    self.uri = uri
    s = users.select(users.c.perm_url == uri)
    r = run(s)
    return r

#returns all letters by an author 
def indexAuthor (self,author):
    self.author = author
    index = users.select(users.c.type == author)
    r =run(index)
    return r

#gets any annotations for a letter - this will come later
def getAnnotation (self,url):
    self.url = url
    annotation = notes.select(notes.c.url == url)
    r = run(annotation)
    return r

#inserts the annotation - this will come later once the templating as been done
def insertAnnotation (self, url):
    self.url = url
    insertNote = notes.insert(notes.c.url == url)
    r = run(insertNote)
    return r

#gets any tags for a letter - this will come later
def getTags (self,url):
    self.url = url
    annotation = tags.select(notes.c.url == url)
    r = run(annotation)
    return r

#inserts the tags - this will come later once the templating as been done
def insertTags (self, url):
    self.url = url
    insertNote = tags.insert(notes.c.url == url)
    r = run(insertNote)
    return r