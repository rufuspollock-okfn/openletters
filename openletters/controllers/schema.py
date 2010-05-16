import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import genshi

from openletters.lib.base import BaseController, render
from openletters.transform import transform_html

log = logging.getLogger(__name__)

class SchemaController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/schema.mako')
        # or, return a response
        c.site_title = "Open Correspondence"
        c.page_title = "Letter schema"
        
        schema = transform_html.output_schema()
        c.letterhtml = genshi.HTML(schema)
        
        if c.letterhtml is None:
            abort(404)
        else:
            return render('schema.html')
