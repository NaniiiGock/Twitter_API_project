import requests

from flask import Flask, render_template, url_for, request
import folium
from geopy.geocoders import Nominatim

def get_info(username):

    '''
    Gets information about followers
    '''
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAMuAZAEAAAAAQbVcaIUIJGtPIg7k9oA%2Bm47xgJ4%3DCtnnFDay5tZkW81CSNmsRu0wRkKctp2sTzYhxM868K0BUrXe5u'
    headers = {'Authorization': f'Bearer {bearer_token}'}
    params = {'screen_name': username, 'count': 200}
    response = requests.get('https://api.twitter.com/1.1/friends/list.json',
                            headers=headers,
                            params=params)
    try:
        return response.json()["users"]
    except KeyError:
        return False

def gett(info):
    """
    function is working with the list of info
    return the total information that
    is used in creating the map
    """
    list1 =[]
    for i in range(len(info)):
        try:
            location = Nominatim(user_agent="app_name").geocode(info[i]["location"])
            list1.append((location.latitude, location.longitude, info[i]['screen_name']))
        except KeyError:
            continue
        except Exception:
            continue
    return list1
# print(gett(get_info("@MaskIlon3")))

def creating_map(list1):
    """
    main part of creating the map
    """
    map = folium.Map()
    point_layer = folium.FeatureGroup(name='coordinates')
    for coordinate in list1:
        lat, lng = coordinate[0], coordinate[1]
        point_layer.add_child(folium.CircleMarker(location=[lat, lng], radius=10,
        popup=coordinate[2],
            tooltip=coordinate[2],
            fill=True,
        color='red',
        fill_opacity=1.0)).add_to(map)
    map.add_child(point_layer)
    map.save('templates/map.html')


app = Flask(__name__)
@app.route("/")
def load_main_page():
    '''
    loading the main page of the site
    '''
    return render_template('index.html')

@app.route("/result", methods=['POST'])
def go_to_map():
    '''
    the function creates the map
    (depending on the username)
    '''
    username = request.form['username']
    creating_map(gett(get_info(username)))
    return render_template('map.html')


app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
