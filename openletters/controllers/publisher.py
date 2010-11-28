import logging, urllib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from openletters.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PublisherController(BaseController):

    def index (self):
        return render('letters/publisherindex.html')
    '''
       Method to return the publisher details in HTML
    '''
    
    def view (self, author=None):
        
        if author is None:
            return render('letters/publisherindex.html')
        else:
            mag = urllib.unquote(author)
            if mag =="Chapman and Hall":
                c.abstract = u"""
                Chapman & Hall was a British publishing house in London, founded in the first half of the 19th century by Edward Chapman and William Hall. Upon Hall's death in 1847, Chapman's cousin Frederic Chapman became partner in the company, of which he became sole manager upon the retirement of Edward Chapman in 1864. In 1868 author Anthony Trollope bought a third of the company for his son, Henry Merivale Trollope. From 1902 to 1930 the company's managing director was Arthur Waugh. In the 1930s the company merged with Methuen, a merger which, in 1955 participated in forming the Associated Book Publishers. The latter was acquired by The Thomson Corporation in 1987.
                Chapman & Hall was sold again in 1998 as part of Thomson Scientific and Professional to Wolters Kluwer, who sold on its well-regarded mathematics and statistics list to CRC Press. Today the name of Chapman & Hall/CRC is used as an imprint for science and technology books by Taylor and Francis, part of the Informa group since 2004.
                Most notably, the company were publishers for Charles Dickens (from 1840 until 1844 and again from 1858 until 1870), and William Thackeray. They continued to publish hitherto unpublished Dickens material well into the 20th century.
                """
                c.mag_url = u"http://en.wikipedia.org/wiki/Chapman_and_Hall"
            else:
                redirect_to(controller='publisher', action='view')
                
            return render('letters/publisher.html') 