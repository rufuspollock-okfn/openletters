import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render
from openletters import model
from openletters.transform import transform_html

log = logging.getLogger(__name__)

class LettersController(BaseController):
    def index(self):
        c.letters = model.Session.query(model.Letter).all()
        return render('letters/index.html')
    
    def view(self, id=None):
        c.letter = model.Session.query(model.Letter).get(id)
        if c.letter is None:
            abort(404)
        return render('letters/view.html')
        
