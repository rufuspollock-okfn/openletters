import logging

import genshi

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render
from openletters import model
from openletters.transform import transform_html

log = logging.getLogger(__name__)

class LettersController(BaseController):
    def index(self):
        c.site_title = "Open Correspondence"
        c.page_title = "Index of letters written by Charles Dickens"
        author = request.params.get('author', '')
        if author:
            # TODO: filter by author
            pass
        else:
            c.letters = model.Session.query(model.Letter).all()
        return render('letters/index.html')
        return render('index.html')
        
    def view(self, id=None):
        c.letter = model.Session.query(model.Letter).get(id)
        if c.letter is None:
            abort(404)
        else:
            return render('letters/view.html')
        
