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
    # listened_by = ndb.StringProperty(repeated=True)

class Playlist(ndb.Model):
    channel = ndb.StringProperty()
    playlist_size = ndb.IntegerProperty(default=0)
    songs_played = ndb.StructuredProperty(Song, repeated=True, required=False)


@app.route('/')
def index():
    return '''
    /save/<name> - returns url_string <br>
    /get/url_string/ - returns data
    '''

@app.route('/channels/', methods=['GET', 'POST'])
def channels():
    if request.method == 'POST':
        pl = Playlist(channel=request.json['channel'])
        playlist_key = pl.put()
        return jsonify({'response': 'ok', 'operation': 'channel_added'})
    else:
        data = {'channels' : []}
        q = Playlist.query()
        for pl in q.fetch():
            data['channels'].append(pl.channel)
        return jsonify(data)

@app.route('/channels/<channel_name>/', methods=['GET', 'POST'])
def channel_details(channel_name):
    if request.method == 'POST':
        # FOR TESTING PURPOSES
        q = Playlist.query(Playlist.channel==channel_name).fetch()
        s = Song.query(Song.song_id==request.json['song_id']).fetch() #TODO: Avoid duplicateds
        if s:
            pl_model = q[0] #TODO: Be sure that fetch only one
            pl_model.songs_played = pl_model.songs_played + s
            pl_model.playlist_size = len(pl_model.songs_played)
            pl_model.put()
            return jsonify({'response': 'ok', 'operation': 'song_added_to_playlist'})
        else:
            return jsonify({'response': 'fail', 'operation': 'song_not_found'})

    else:
        data = {}
        q = Playlist.query(Playlist.channel==channel_name).fetch()
        pl = q[0]
        data['channel'] = pl.channel
        data['playlist'] =  []
        for song in pl.songs_played:
            print(str(song))
            song_data = {
                'song_id': song.song_id,
                'name': song.name,
                'added_by': song.added_by,
                'updubs': song.updubs,
                'downdubs': song.downdubs,
            }
            data['playlist'].append(song_data)
        data['playlist_size'] = pl.playlist_size

        return jsonify(data)

@app.route('/songs/', methods=['GET', 'POST'])
def get_all_song():
    if request.method == 'POST':
        print(request.json)
        song = Song(song_id=song_id, name=name, added_by=added_by, updubs=updubs, downdubs=downdubs)
    song_key = song.put()
    return song_key
        create_and_save_song(
            request.json['song_id'],
            request.json['name'],
            request.json['added_by'],
            request.json['updubs'],
            request.json['downdubs'])
        return 'Done'
    else:
        data = {'songs' : []}
        s = Song.query()

        for s in s.fetch():
            song_data = {
                'song_id': s.song_id,
                'name': s.name,
                'added_by': s.added_by,
                'updubs': s.updubs,
                'downdubs': s.downdubs,
            }
            data['songs'].append(song_data)

        return jsonify(data)


@app.route('/songs/<song_id>/', methods=['GET'])
def get_song_by_id(song_id):
    s = Song.query(Song.song_id==song_id).fetch()
    s = s[0] #TODO: Avoid duplicated
    song_data = {
        'song_id': s.song_id,
        'name': s.name,
        'added_by': s.added_by,
        'updubs': s.updubs,
        'downdubs': s.downdubs,
    }
    return jsonify(song_data)

# TO CHANGE
@app.route('/playlist/anime/delete/', methods=['GET'])
def delete_anime_playlist():
    q = Playlist.query(Playlist.room=='anime')
    for pl in q.fetch():
        pl.key.delete()
    return 'Deleted'