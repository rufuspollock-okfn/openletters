from openletters.tests import *

class TestLettersController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='letters', action='index'))
        # Test response...
