from openletters.tests import *
import openletters.model as model

class TestLettersController(TestController):
    @classmethod
    def setup_class(self):
        Fixtures.setup()

    @classmethod
    def teardown_class(self):
        Fixtures.teardown()

    def test_index(self):
        response = self.app.get(url(controller='letters', action='index'))
        assert 'Mr MaCready' in response
        res2 = response.click('Mr MaCready.*')
        assert 'To: Mr MaCready' in res2

    def test_view(self):
        letter = Fixtures.letter()
        response = self.app.get(url(controller='letters', action='view',
            id=letter.id))
        print letter.correspondent
        restext = response.body.decode('utf8').encode('ascii', 'ignore')
        # print unicode(response.body, encoding='utf8')
        assert 'To: %s' % letter.correspondent in response, restext

