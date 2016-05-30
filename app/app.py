from flask import Flask
import requests
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world'


@app.route('/<room_url>/playlist/')
def playlist(room_url):
    room_id = get_room_id(room_url)
    url = 'https://api.dubtrack.fm/room/%s/playlist/history' % room_id
    r = requests.get(url)
    return str(r.content)


if __name__ == '__main__':
    app.run()

def get_room_id(room_url):
    url = 'https://api.dubtrack.fm/room/%s/' % room_url
    r = requests.get(url)
    result = r.json()['data']['_id']
    return str(result)