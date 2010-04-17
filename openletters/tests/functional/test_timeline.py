from openletters.tests import *

class TestTimelineController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='timeline', action='index'))
        # Test response...
