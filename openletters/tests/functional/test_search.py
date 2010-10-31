from openletters.tests import *

class TestSearchController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='search', action='index'))
        assert 'search' in response
        
