from sqlalchemy import create_engine, Table, Column, Integer, UnicodeText, MetaData, ForeignKey
from sqlalchemy import orm

from meta import engine, metadata

'''
  Function to set up the books table
  Contains title data 
  two publication dates (the second one is for ending if the book was serialised)
  two aka fields if the book is known by another name
  description is a brief description of the book
  url is a wikipedia / dbpedia url - might change in future
'''

books_table = Table('books', metadata,
                     Column('book_id', Integer, primary_key=True),
                     Column('book_title', UnicodeText), 
                     Column('book_pub', UnicodeText),
                     Column('book_end_pub', UnicodeText),
                     Column('aka', UnicodeText),
                     Column('aka2', UnicodeText),
                     Column('description', UnicodeText),
                     Column('url', UnicodeText),
                     Column('source', UnicodeText),
                     )

class Book(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

orm.mapper(Book, books_table)
