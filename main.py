from flask import Flask, request, render_template, redirect, url_for
import requests_toolbelt.adapters.appengine # needed to use requests with GAE
from flask import jsonify # pretty json responses
from gcloud import datastore
from pubnub import Pubnub
import requests
import datetime
import gcloud
import json

YOUR_CHOICE_CHANNEL = 'dubtrackfm-anime'
PROJECT_NAME = 'txomon-demo-1328'
client = None

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

def generateEntities():
    global client
    client = datastore.Client(PROJECT_NAME)

    song = datastore.Entity(client.key('Song', '1'))
    result = json.loads('''
        {
            "playlist": [
                {
                    "_id": 13123235,
                    "name": "River"
                },
                {"2":"hello"},
                {"3":"hello"},
                {"4":"hello"}
            ]
        }
    ''')
    song.update({
            'type': 'Personal',
            'done': False,
            'priority': 4,
            'description': result
    })

    client.put(song)

#generateEntities()
#my_obj = {'key-1': 'value-1', 'key-2': 'value-2'}
#entity = MyEntity(name="my-name", obj=my_obj)
#entity.put()

@app.route('/api/v1/room/<room_url>/playlist/')
def api_playlist(room_url):
    
    return jsonify(result)

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
    return 'Hello'

@app.route('/api/v1/room/<room_url>/queue/insert/')
def api_insert_into_queue(room_url):
    pass

def check_message(message):
    pass

#app.run(debug=True)