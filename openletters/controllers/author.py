import logging, urllib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

from openletters.transform.transform_json import json_transform
from openletters.transform.transform_xml import xml_transform
from openletters.transform.transform_rdf import rdf_transform

log = logging.getLogger(__name__)

class AuthorController(BaseController):
 
    def index (self):
        c.author = "Charles Dickens"
        return render('letters/authorindex.html')
        
    '''
       Action to return the author and type. If no author, return the index
    '''
    def view (self, author=None):
        c.author = "Charles Dickens"
        if author is None: 
            return render('letters/authorindex.html')
        else:
            c.author = u"Charles Dickens"
            c.born = u"7 February 1812"
            c.died = u"9 June 1870"
            c.abstract = u"Charles John Huffam Dickens, pen-name 'Boz', was the most popular English novelist of the Victorian era, and one of the most popular of all time, responsible for some of English literature's most iconic characters. Many of his novels, with their recurrent theme of social reform, first appeared in periodicals and magazines in serialised form, a popular format for fiction at the time. Unlike other authors who completed entire novels before serial production began, Dickens often wrote them while they were being serialized, creating them in the order in which they were meant to appear. The practice lent his stories a particular rhythm, punctuated by one 'cliffhanger' after another to keep the public looking forward to the next installment. The continuing popularity of his novels and short stories is such that they have never gone out of print. His work has been praised for its mastery of prose and unique personalities by writers such as George Gissing and G. K. Chesterton, though the same characteristics prompted others, such as Henry James and Virginia Woolf, to criticize him for sentimentality and implausibility."
            c.author_url = u"http://en.wikipedia.org/wiki/Charles_Dickens"
            return render('letters/author.html')
        
    def resource (self, author=None, correspondent=None):
        
        if author is None:
            abort(404)
        else:
            title = str(urllib.unquote(author))
            if correspondent == "rdf":
                response.headers['Content-Type'] = 'text/xml; charset=utf-8'
                rdf = rdf_transform()
                return rdf.create_author(title)