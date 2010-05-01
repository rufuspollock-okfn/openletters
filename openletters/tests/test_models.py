from openletters import model

class TestModel:
    def test_01(self):
        date = u'18th Aug'
        vol = u'1'
        text = u'xxxx'
        letter1 = model.Letter(volume=vol, letter_text=text, letter_date=date)
        model.Session.add(letter1)
        model.Session.commit()
        id = letter1.id
        model.Session.remove()
        let2 = model.Session.query(model.Letter).get(id)
        assert let2.letter_text == text

