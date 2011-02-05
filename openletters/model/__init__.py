"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

import meta
from meta import Session
from letter import letter_table, Letter, source_table, Source
from books import books_table, Book
from places import location_table, Location

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.metadata.bind = engine
    meta.engine = engine


class Repository(object):
    def create_db(self):
        meta.metadata.create_all()
    
    def clean_db(self):
        meta.metadata.drop_all()

    def rebuild_db(self):
        self.clean_db()
        self.create_db()

repo = Repository()
