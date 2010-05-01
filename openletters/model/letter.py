'''creates the tables - to be extended at a later date 19 April 2010'''
from sqlalchemy import create_engine, Table, Column, Integer, UnicodeText, MetaData, ForeignKey
from sqlalchemy import orm

from meta import engine, metadata

lettersTbl = Table('letters', metadata,
    Column('id', Integer, primary_key=True),
    Column('volume', Integer),
    Column('type', UnicodeText),
    Column('perm_url', UnicodeText),
    Column('salutation', UnicodeText),
    Column('correspondent', UnicodeText),
    Column('letter_text', UnicodeText),
    Column('letter_date', UnicodeText),                 
)
letter_table = lettersTbl


class Letter(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)


orm.mapper(Letter, lettersTbl)

