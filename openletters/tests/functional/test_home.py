from openletters.tests import *

class TestHomeController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='home', action='index'))
        assert 'Open Correspondence' in response
        assert 'Dickens' in response

