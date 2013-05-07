from openletters.format import formatter
from nose.tools import *
import json

class TestFormatTestController():
    '''
       Function to test the formatting of the data
    '''
    def setup_funct(self):
        self.data = {'name' : 'J MacCready' , 'author' : 'an author'}
        
    def teardown_func(self):
        pass
    
    def testFormatJson(self):
        form = formatter()
        encode_json_string = form.to_json(self.data)
        decode_json_string = json.loads(encode_json_string)
        assert decode_json_string['name'] == 'J MacCready'
        assert decode_json_string['author'] == 'an author'