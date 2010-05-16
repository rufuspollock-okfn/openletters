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
        
        #todo: we need a method for this when there are more authors
        index = "<p>This is an index of authors whose letters are on the Open Correspondence site</p>"
        index += '<p><a href="author?author=Dickens">Charles Dickens</a>'
            
        c.letterhtml = genshi.HTML(index)
        
        if c.letterhtml is None:
            abort(404)
        else:
            return render('index.html')
        
    def author(self):
        c.site_title = "Open Correspondence"
        c.page_title = "Index of letters written by Charles Dickens"
        author = request.params.get('author', '')
        
        #todo: we need a method for this when there are more authors
        index = transform_html.output_author_index(author)
            
        c.letterhtml = genshi.HTML(index)
        
        if c.letterhtml is None:
            abort(404)
        else:
            return render('index.html')
        
    def text(self):
        #should this be pushed into a method to create a better title?
        c.site_title = "Open Correspondence"
        c.page_title = "Letter written by Charles Dickens"
        author = request.params.get('letter', '')
        letter = transform_html.output_letter(author)
        c.letterhtml = genshi.HTML(letter)

        if c.letterhtml is None:
            abort(404)
        else:
            return render('text.html')

        
def render_resource(html_stream):
      tfileobj = html_stream.get_stream()
      ttext = tfileobj.read()
       
      return ttext