'''creates the tables - to be extended at a later date 19 April 2010'''
from sqlalchemy import create_engine, Table, Column, Integer, UnicodeText, MetaData, ForeignKey
from sqlalchemy import orm

from meta import engine, metadata

letter_table = Table('letters', metadata,
    Column('id', Integer, primary_key=True),
    Column('volume', Integer),
    Column('type', UnicodeText),
    Column('perm_url', UnicodeText),
    Column('salutation', UnicodeText),
    Column('correspondent', UnicodeText),
    Column('letter_text', UnicodeText),
    Column('letter_date', UnicodeText),                 
)

source_table = Table('sources', metadata,
                     Column('t_id', Integer, primary_key=True),
                     Column('source_id', Integer), 
                     Column('title', UnicodeText),
                     Column('author', UnicodeText),
                     Column('publn_data', UnicodeText),
                     Column('publn_date', UnicodeText),
                     Column('s_url', UnicodeText),

                     )


class Letter(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
            
class Source(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

orm.mapper(Letter, letter_table)
orm.mapper(Source, source_table)

