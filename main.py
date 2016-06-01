from flask import Flask, request, render_template, redirect, url_for
import requests_toolbelt.adapters.appengine # needed to use requests with GAE
from flask import jsonify # pretty json responses
from pubnub import Pubnub
import requests
import json
import pymongo
from google.appengine.ext import ndb

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

class Song(ndb.Model):
    song_id = ndb.StringProperty()
    name = ndb.StringProperty()
    added_by = ndb.StringProperty()
    updubs = ndb.IntegerProperty()
    downdubs = ndb.IntegerProperty()
    # listened_by

def create_and_save_model(song_id, name, added_by, updubs, downdubs):
    song = Song(song_id=song_id, name=name, added_by=added_by, updubs=updubs, downdubs=downdubs)
    song_key = song.put()
    return song_key


def get_url_safe_key(sandy_key):
    url_string = sandy_key.urlsafe()
    return url_string

def get_model_from_url_safe_key(url_string):
    sandy_key = ndb.Key(urlsafe=url_string)
    sandy = sandy_key.get()
    return sandy

@app.route('/')
def index():
    return '''
    /save/<name> - returns url_string <br>
    /get/url_string/ - returns data
    '''

@app.route('/songs/', methods=["GET", "POST"])
def get_all_song():
    if request.method == "POST":
        create_and_save_model(
            request.data['song_id'],
            request.data['name'],
            request.data['added_by'],
            request.data['updubs'],
            request.data['downdubs'])
    else:
        q = Song.query()
        return str(q)

@app.route('/songs/<song_id>/')
def get_song_by_id(song_id):
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