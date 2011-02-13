from sqlalchemy import create_engine, Table, Column, Integer, UnicodeText, MetaData, ForeignKey
from sqlalchemy import orm

from meta import engine, metadata



location_table = Table('location', metadata,
                     Column('locationid', Integer, primary_key=True),
                     Column('placeid', UnicodeText), 
                     Column('latitude', UnicodeText), 
                     Column('longitude', UnicodeText),
                     Column('url', UnicodeText),
                     Column('source', UnicodeText),
                     )

class Location(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

orm.mapper(Location, location_table)