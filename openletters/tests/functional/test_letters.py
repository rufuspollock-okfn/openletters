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
            author = 'dickens',
            correspondent = 'Lord Lytton',
            id='879'))
        print letter.correspondent
        restext = response.body.decode('utf8').encode('ascii', 'ignore')
        # print unicode(response.body, encoding='utf8')
        assert '[Sidenote: %s ]' % letter.correspondent in response, restext

    def test_correspondent(self):
        letter = Fixtures.letter()
        response = self.app.get(url(controller='letters', action="correspondent", 
            author="Miss Hogarth" ))
        assert 'Miss Hogarth' in response