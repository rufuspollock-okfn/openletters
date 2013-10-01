'''
   Will become access to Elastic Search
   
   DAO to read the JSON file
'''
import json

def getdataindex():
    """
       Get the file
    """
    data = __getdata()
    authors = set()
    for lines in data['Charles_Dickens']:
        authors.add(lines['correspondent'])
    authors = list(authors)
    # put it into a list and then reorder
    return authors

def getdataauthor(correspondent):
    """
       Get the file
    """
    data = __getdata()
    authors = {}
    
    for lines in data['Charles_Dickens']:
        if lines['correspondent'] == correspondent:
            authors[lines['id']] =str(lines['date'])
            
    return authors

def getletter(letterid):
    """
       Get the file
    """
    data = __getdata()
    letter = {}

    for lines in data['Charles_Dickens']:
        if lines['id'] == letterid:
            letter = {'correspondent':lines['correspondent'], 
                      'place':lines['place'], 
                      'date':lines['date'],
                      'letter':lines['letter']}
            
    return letter

def getplacemap():
    
    d = __getplacedata()
    
    place = []
    for lines in d['Charles_Dickens']:
        place.append({
            "lon" : lines['lon'], 
            "lat" : lines['lat']
                 })
    print place
    # put it into a list and then reorder
    return json.dumps({'geo':place})   

def getplaceindex():
    '''
       Fetch the places and put into a basic index
    '''
    d = __getdata()
    
    place = set()
    for lines in d['Charles_Dickens']:
        place.add(lines['place'])
    place = list(place)
    return place   

def getplace(place):
    """
       Get the file
    """
    # Get the place location
    d = __getplacedata()
    # get the letter location
    data = __getdata()
    places = {}
    
   # for points in d['Charles_Dickens']:
   #     if points['url'] == place:
   #         places['place'] = {
   #             'lat' : points['lat'],
   #             'lon' : points['lon']
   #         }
            

    for lines in data['Charles_Dickens']:
 
        if lines['place'] == place:

            places[lines['id']] = {'correspondent':lines['correspondent'], 
                      'date':lines['date'],
                      'place':lines['place']}
    
    return places

def __getdata():
    '''
       Private function to open the JSON file
    '''
    return json.loads(open('../data/dickensletter.json', 'r').read())

def __getplacedata():
    '''
       Private function to open the JSON file
    '''
    return json.loads(open('../data/place.json', 'r').read())