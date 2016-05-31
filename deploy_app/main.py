from flask import Flask, request, render_template, redirect, url_for
import requests
from pubnub import Pubnub
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()
app = Flask(__name__)

from flask import jsonify

def make_get_request(url):
    response = requests.get(url)
    return response

def get_room_id(room_url):
    """Returns id of the room."""
    url = 'https://api.dubtrack.fm/room/%s/' % room_url
    r = make_get_request(url)
    return r.json()['data']['_id']

def get_room_playlist(room_id):
    """Returns the playlist history of the room (20 songs)."""
    url = 'https://api.dubtrack.fm/room/%s/playlist/history' % room_id
    r = make_get_request(url)
    return r.json()

def get_room_active_song(room_id):
    """Returns the current song."""
    url = 'https://api.dubtrack.fm/room/%s/playlist/active' % room_id
    r = make_get_request(url)
    try:
        if r.json()['data']['song']:
            return r.json()
    except KeyError:
        return None

def get_username_by_id(user_id):
    """Returns the username."""
    url = 'https://api.dubtrack.fm/user/%s' % user_id
    r = make_get_request(url)
    return r.json()

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST' and request.form['room_name']:
        return redirect(url_for('room_info', room_url=request.form['room_name']))
    else:
        return render_template('index.html')

@app.route('/<room_url>/')
def room_info(room_url):
    global pubnub
    channel = 'dubtrackfm-' + room_url
    pubnub.subscribe(channels=channel, callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)
    print("Suscribed to something")
    room_id = get_room_id(room_url)

    active_song = None
    while(active_song == None):
        active_song = get_room_active_song(room_id)

    room_playlist = get_room_playlist(room_id)
    active_song_user = get_username_by_id(active_song['data']['song']['userid'])    
    data = {
        'active_song' : active_song,
        'room_playlist': room_playlist,
        'active_song_user' : active_song_user
    }
    return render_template('room.html', data=data)

@app.route('/<room_url>/playlist/')
def playlist(room_url): 
    room_id = get_room_id(room_url)
    result = get_room_playlist(room_id)
    return jsonify(result)

@app.route('/<room_url>/active/')
def active(room_url):
    room_id = get_room_id(room_url)
    result = get_room_active_song(room_id)
    return jsonify(result)


pubnub = Pubnub(publish_key="", subscribe_key="sub-c-2b40f72a-6b59-11e3-ab46-02ee2ddab7fe")

def callback(message, channel):
    print(message)
  
  
def error(message):
    print("ERROR : " + str(message))
  
  
def connect(message):
    print("CONNECTED")
    #print(pubnub.publish(channel='my_channel', message='Hello from the PubNub Python SDK'))
  
    
def reconnect(message):
    print("RECONNECTED")
  
  
def disconnect(message):
    print("DISCONNECTED")
  

#app.run()