from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
'''creates the tables - to be extended at a later date 19 April 2010'''
metadata = MetaData()

engine = create_engine('engine://user:pword@localhost/py_dickens', echo=True)

lettersTbl = Table('letters', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('volume', Integer),
                   Column('type', String(20)),
                   Column('perm_url', String(50)),
                   Column('salutation', String(75)),
                   Column('correspondent', String(50)),
                   Column('letter_text', String(10000)),
                   Column('letter_date', String(20)),                 
)

metadata.create_all(engine)