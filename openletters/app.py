import json, urllib2

from flask import Flask, app, render_template, request, url_for

import dao

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schema')
def schema():
    return render_template('schema.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/correspondents/', methods=['GET'])
@app.route('/correspondent/<name>', methods=['GET'])
# '@todo implement limiting by author
# @app.route('/correspondent/<name>/<author>', methods=['GET'])
def author(name=None):
    
    if name is None:
        name = dao.getdataindex()

        if request.args.get('json', None) is not None:
            return json.dumps([{'name': x, 'path': url_for('author', name=x)} for x in sorted(name)])
        return render_template('authorindex.html', name=sorted(name))
    else:
        name = urllib2.unquote(name)
        dates = dao.getdataauthor(name)
        if request.args.get('json', None) is not None:
            return json.dumps([{'date': date, 'path': url_for('letter', letterid=id)} for id, date in dates.iteritems()])
        return render_template('author.html', dates=dates, name=name)        
    
@app.route('/letter/<int:letterid>', methods=['GET'])
def letter(letterid=None):
    
    if letterid is None:
        return render_template('letterindex.html')
    else:
        letter = dao.getletter(letterid)
        if request.args.get('json', None) is not None:
            return json.dumps(letter)
        return render_template('letter.html', letter=letter) 
    
  
@app.route('/place/', methods=['GET'])    
@app.route('/place/<location>', methods=['GET'])
def place(location=None):

    if location is None:
        location = dao.getplaceindex()
        latlon = dao.getplacemap()
        if request.args.get('json', None) is not None:
            return json.dumps([{'place': x, 'path': url_for('place', location=x)} for x in sorted(location)])
        return render_template('placemap.html', location=sorted(location))
        #return render_template('placemap.html', place=location, latlon=latlon)
    else:
        letter = dao.getplace(location)
        if request.args.get('json', None) is not None:
            return json.dumps([dict({'path': url_for('letter', letterid=k)}.items() + v.items()) for k,v in letter.iteritems()])
        return render_template('placeindex.html', place=letter, location=location)  

if __name__ == '__main__':
    app.run(debug=True)
