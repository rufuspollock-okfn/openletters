import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import genshi

from openletters.lib.base import BaseController, render
from openletters import model
from openletters.transform import transform_json

log = logging.getLogger(__name__)

class TimelineController(BaseController):
    def index(self):
        return render('timeline/index.html')

