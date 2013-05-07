from flask import Flask
from flask.ext.testing import TestCase
#from nose.test import *

class TestTemplates(TestCase):
    
    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app
    
    def test_index(self):
        '''
            Function to test the main page
        '''
        response = self.client.get("/")
        self.assert200(response)
        self.assertEquals('hello', response)
        
    def test_correspondent_listing(self):
        '''
            Function to test the Correspondent listing
        '''
        response = self.client.get("/correspondent/J%20MacCready")
        self.assertEquals('hello', response)
        
    def test_correspondent_author_listing(self):
        '''
            Function to test the Correspondent and Author listing
        '''
        response = self.client.get("/correspondent/J%20MacCready/Charles%Dickens")
        self.assertEquals('hello', response)