from flask import Flask, app, render_template, request

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

        return render_template('authorindex.html', name=sorted(name))
    else:
        name = name.replace('%20', ' ')
        dates = dao.getdataauthor(name)
        return render_template('author.html', dates=dates, name=name)        
    
@app.route('/letter/<int:letterid>', methods=['GET'])
def letter(letterid=None):
    
    if letterid is None:
        return render_template('letterindex.html')
    else:
        letter = dao.getletter(letterid)
        return render_template('letter.html', letter=letter) 
    
  
@app.route('/place/', methods=['GET'])    
@app.route('/place/<location>', methods=['GET'])
def place(location=None):

    if location is None:
        location = dao.getplaceindex()
        latlon = dao.getplacemap()
        print latlon
        return render_template('placemap.html', location=sorted(location))
        #return render_template('placemap.html', place=location, latlon=latlon)
    else:
        letter = dao.getplace(location)
        return render_template('placeindex.html', place=letter, location=location)  
if __name__ == '__main__':
    app.run(debug=True)