import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

log = logging.getLogger(__name__)

class HomeController(BaseController):
    def index(self):
        return render('home/index.html')

    def gallery(self):
        return render('home/index.html')

    def schema(self):
        return render('home/schema.html')
   
    def help(self):
        return render('home/help.html')
