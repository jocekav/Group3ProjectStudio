from flask import Flask, render_template, redirect, request, url_for
import spotifyAuthentication
import spotifyPlayback
import spotifyPlayback2
import json
import spotipy
import time
import threading
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

global currSong
currSong = 0
global playFlag
global event
event = threading.Event()

@app.route("/")
def index():
    return render_template('home.html', title="Home")

@app.route("/callback/")
def callback():
    return redirect(spotifyAuthentication.getAuth())

@app.route("/player/", methods= ['GET', 'POST'])
def player():
    userToken = spotifyAuthentication.getUserToken(request.args['code'])
    token = {'userToken': userToken[0]}
    return render_template('temp.html', token=token, songTitle={'Superstition'})

@app.route("/initPlayer")
def initPlayer():
    spotifyPlayback2.initPlayer()
    return 'nothing'

@app.route("/startPlayback")
def startPlayback():
    global currSong
    global playFlag
    global event
    playFlag = True
    #get list from Rose
    playlist = ['spotify:track:0oQc0F6KUE7QY7k5TU6bic', 'spotify:track:7yBbV2k2S2uhaQc24NF2xt']
    while (playFlag):
        # progress = spotifyPlayback2.getProgress()
        # if progress is 'NoneType':
        #     progress = 0
        duration = spotifyPlayback2.getSongLength(playlist[currSong])
        spotifyPlayback2.startPlayback(playlist[currSong])
        wait = float((duration))/1000.0
        event.wait(wait)
        # progress = spotifyPlayback2.getProgress()
        # if(progress == duration):
        currSong += 1
    # return (title=title, albumArt=art)
    # return render_template('temp.html', songTitle='testTest')
    return 'nothing'

@app.route("/pausePlayback")
def pausePlayback():
    global playFlag
    playFlag = False
    spotifyPlayback2.pausePlayback()
    event.set()
    print(spotifyPlayback2.getSongInfo('spotify:track:0oQc0F6KUE7QY7k5TU6bic'))
    return 'nothing'

@app.route('/addQueue')
def addQueue():
    spotifyPlayback.addSongToQueue('spotify:track:5aaUXcrsXI477I93yBE8lu')
    return 'nothing'

@app.route('/nextTrack')
def nextTrack():
    spotifyPlayback.nextSong()
    return 'nothing'

if __name__ == "__main__":
    app.run(debug=True, port=5000)