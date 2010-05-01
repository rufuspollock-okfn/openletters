import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters.transform import transformJson

log = logging.getLogger(__name__)

class DataController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/data.mako')
        # or, return a response
        author =  request.params['author']
        timeline = transformJson.authorTimeline(author)

        
        return timeline
