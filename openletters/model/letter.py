'''creates the tables - to be extended at a later date 19 April 2010'''
from sqlalchemy import create_engine, Table, Column, Integer, UnicodeText, MetaData, ForeignKey
from sqlalchemy import orm

from meta import engine, metadata

letter_table = Table('letter', metadata,
    Column('id', Integer, primary_key=True),
    Column('volume', Integer),
    Column('type', UnicodeText),
    Column('perm_url', UnicodeText),
    Column('salutation', UnicodeText),
    Column('correspondent', UnicodeText),
    Column('letter_text', UnicodeText),
    Column('letter_date', UnicodeText),                 
)


class Letter(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)


orm.mapper(Letter, letter_table)

