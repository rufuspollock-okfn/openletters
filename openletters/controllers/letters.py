import logging

import genshi

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render
from openletters import model
from openletters.transform import transform_html
from openletters.parseText import parse_text, parse_date

log = logging.getLogger(__name__)

class LettersController(BaseController):
    def index(self):
        c.site_title = "Open Correspondence"
        
        author = request.params.get('author', '')
        if author:
            c.page_title = "Index of letters written by Charles Dickens"
            c.letters = model.Session.query(model.Letter).filter(model.Letter.type == author)
        else:
            c.page_title = "Index of letters"
            c.letters = model.Session.query(model.Letter).all()
        return render('letters/index.html')
        return render('index.html')
        
    def view(self, id=None):
        c.letter = model.Session.query(model.Letter).get(id)

        if c.letter is None:
            abort(404)
        else:
            return render('letters/view.html')
        