from openletters.tests import *

class TestPublisherController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='publisher', action='index'))
        assert 'Chapman' in response