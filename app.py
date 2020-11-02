from flask import Flask, render_template, redirect, request, url_for
import spotifyAuthentication
import spotifyPlayback
import spotifyPlayback2
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth


app = Flask(__name__)

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
    spotifyPlayback2.startPlayback('spotify:track:4N0TP4Rmj6QQezWV88ARNJ')
    return 'nothing'

@app.route("/pausePlayback")
def pausePlayback():
    spotifyPlayback2.pausePlayback()
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