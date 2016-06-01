from flask import Flask, request, render_template, redirect, url_for
import requests_toolbelt.adapters.appengine # needed to use requests with GAE
from flask import jsonify # pretty json responses
from pubnub import Pubnub
import requests
import json
import pymongo
YOUR_CHOICE_CHANNEL = 'dubtrackfm-anime'

app = Flask(__name__)

def callback(message, channel):
    if message['type'] == 'room_playlist-update':
        print(message)
    # if message['type']:
        # ...
    
def error(message):
    print("ERROR : " + str(message))
    
def connect(message):
    print("Connected")
  
def reconnect(message):
    print("Reconnected")
  
def disconnect(message):
    print("Disconnected")

#pubnub = Pubnub(publish_key="", subscribe_key="sub-c-2b40f72a-6b59-11e3-ab46-02ee2ddab7fe")
#pubnub.subscribe(channels=YOUR_CHOICE_CHANNEL, callback=callback, error=callback,
#                 connect=connect, reconnect=reconnect, disconnect=disconnect)

from google.appengine.ext import ndb

class Account(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.StringProperty()
    email = ndb.StringProperty()

def create_model_using_keyword_arguments(name):
    sandy = Account(
        username='Sandy', userid=name, email='sandy@example.com')
    return sandy

def save_model(sandy):
    sandy_key = sandy.put()
    return sandy_key

def get_url_safe_key(sandy_key):
    url_string = sandy_key.urlsafe()
    return url_string

def get_model_from_url_safe_key(url_string):
    sandy_key = ndb.Key(urlsafe=url_string)
    sandy = sandy_key.get()
    return sandy

@app.route('/api/v1/room/<room_url>/playlist/')
def api_playlist(room_url):
    pass

@app.route('/api/v1/song/<song_id>/')
def api_song_details(song_id):
    result = json.loads('''
    {
            "song": {
                "_id": 13123235,
                "name": "River",
                "added_by": "Willy",
                "updubs": 523,
                "downdubs": 2312,
                "listened_by": [
                    {
                        "user_id": 3214124,
                        "username": "Rallys"
                    
                    },
                    {
                        "user_id": 3214124,
                        "username": "Rallys"
                    
                    },
                    {
                        "user_id": 3214124,
                        "username": "Rallys"
                    
                    }
                ]
            }
        }
    ''')
    return jsonify(result)

# API END-POINTS
@app.route('/')
def index():
    return '''
    /save/<name> - returns url_string <br>
    /get/url_string/ - returns data
    '''

@app.route('/get/<url_string>/')
def get_key(url_string):
    sandy = get_model_from_url_safe_key(url_string)
    return str(sandy)

@app.route('/save/<name>')
def save(name):
    sandy = create_model_using_keyword_arguments(name)
    x = save_model(sandy)
    return get_url_safe_key(x)


@app.route('/api/v1/room/<room_url>/queue/insert/')
def api_insert_into_queue(room_url):
    pass

def check_message(message):
    pass

#app.run(debug=True)