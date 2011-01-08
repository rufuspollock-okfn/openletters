import logging, xapian, re, urllib

from pylons import request, response, session, tmpl_context as c, config

from openletters.lib.base import BaseController, render
from openletters import model

log = logging.getLogger(__name__)

"""
   Developed from the Open Shakespeare code and a useful tutorial at:
   http://invisibleroads.com/tutorials/xapian-search-pylons.html
   to get the text extracts. 
   TODO: start and stop the text on a full word boundary. 
"""
class SearchController(BaseController):

    def index(self):
        
        return render('letters/text.html')
    
    def query(self):
        # Load queryString
        queryString = request.GET.get('q', '').strip()
        # If queryString exists,
        if queryString:
            # Connect to database
            try:
                database = xapian.Database(config['xapian_host'])
                #database = xapian.WritableDatabase(config['xapian_host'], xapian.DB_CREATE_OR_OPEN)
               # database = xapian.remote_open(config['xapian_host'], config['xapian_port'])
            except xapian.DatabaseOpeningError:
                return 'Cannot open database at ' + config['xapian_host'] + "on port:" + config['xapian_port']
            # Parse query string
            queryParser = xapian.QueryParser()
            queryParser.set_stemmer(xapian.Stem('english'))
            queryParser.set_database(database)
            queryParser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
            query = queryParser.parse_query(queryString)
            # Set offset and limit for pagination
            offset, limit = 0, database.get_doccount()
            # Start query session
            enquire = xapian.Enquire(database)
            enquire.set_query(query)
            # Display matches
            matches = enquire.get_mset(offset, limit)
            
            c.matches = [ SearchResult.from_match(m,queryString ) for m in matches ]
            c.total = matches.get_matches_estimated()
            # Render
            return render('letters/text.html')

class SearchResult(object):
    def __init__(self, snippet, letterid, correspondent, date):
        self.snippet = snippet
        self.correspondent = correspondent
        self.letterid = letterid
        self.date = date

    @classmethod
    def from_match(cls, m, query):
        text = SearchResult.process(query, m.document.get_data())
        snippet = unicode(text,'latin-1')
        lineno = m.docid
        query_string = model.Session.query(model.Letter).filter(model.Letter.id == lineno)
        
        for letter in query_string:
            letterid =  letter.type + "/" + urllib.quote(letter.correspondent) + "/" + str(lineno)
            correspondent = letter.correspondent
            date = letter.letter_date
            

        return cls(snippet, letterid, correspondent, date)

    @classmethod
    def process(cls, queryString, content):

        extractLength = 40
        # Parse query
        queryParser = xapian.QueryParser()
        queryParser.set_stemmer(xapian.Stem('english'))
        queryParser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        query = queryParser.parse_query(queryString)
        
        # Parse content after replacing non-alphanumeric characters with spaces
        queryParser.parse_query(re.sub('\W', ' ', content).lower())
        # Create search pattern
        documentTerms = sum([list(queryParser.unstemlist(x)) for x in set(query)], [])
        if not documentTerms:
            documentTerms = set(query)
        pattern = re.compile(r'\b(%s)\b' % '|'.join(re.escape(x) for x in documentTerms), re.IGNORECASE)
        if not queryString:
            extract = content

        extractIntervals = []
        extractLengthHalved = extractLength / 2
         # For each matchInterval,
        for match in pattern.finditer(content):
             # Prepare
             mStart = max(0, match.start() - extractLengthHalved)
             mEnd = min(len(content), match.end() + extractLengthHalved)
            # Load extracts
             SearchResult.absorbInterval((mStart, mEnd), extractIntervals)

        extract = " ... ".join(content[eStart:eEnd].strip() for eStart, eEnd in extractIntervals)
        
        return extract

    @classmethod
    def absorbInterval(cls, (mStart, mEnd), extractIntervals):
        'Merge overlapping intervals'
        # For each extractInterval,
        for eIndex, (eStart, eEnd) in enumerate(extractIntervals):
            # If the matchInterval is contained in an existing extractInterval,
            if eStart <= mStart and eEnd >= mEnd:
                # Ignore it because we have it already
                return
            # If the matchInterval overlaps the left side of extractInterval,
            elif mEnd > eStart and mEnd < eEnd:
                # Extend the extractInterval in that direction
                extractIntervals[eIndex] = mStart, eEnd
                return
            # If the matchInterval overlaps the right side of extractInterval,
            elif mStart > eStart and mStart < eEnd:
                # Extend the extractInterval in that direction
                extractIntervals[eIndex] = eStart, mEnd
                return
        # The matchInterval does not overlap any existing extractInterval
        extractIntervals.append((mStart, mEnd))
