from openletters.tests import *

class TestDataController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='data', action='index'))
        # Test response...
