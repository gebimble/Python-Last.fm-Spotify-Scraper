#! /usr/bin/env python

import pylast
import pprint
import os
import subprocess
import spotipy
import time
import datetime
import spotipy.util as util

## You have to have your own unique two values for API_KEY and API_SECRET
## Obtain yours from http://www.last.fm/api/account for Last.fm

with open('lastAPI_example','r+') as f:
    lines = f.readlines()
    API_KEY = lines[0].split(' :')
    API_KEY = API_KEY[1].strip()
    API_SECRET = lines[1].split(' :')
    API_SECRET = API_SECRET[1].strip()
    lines =[]

with open('spotAPI_example','r+') as f:
    lines = f.readlines()
    SPOTIPY_CLIENT_ID = lines[0].split(' : ')
    SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID[1].strip()
    SPOTIPY_CLIENT_SECRET = lines[1].split(' :')
    SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET[1].strip()
    SPOTIPY_REDIRECT_URI = lines[2].split(' :')
    SPOTIPY_REDIRECT_URI = SPOTIPY_CLIENT_SECRET[1].strip()
    lines = []

## In order to perform a write operation you need to authenticate yourself
with open('lastUserData_example','r+') as f:
    lines = f.readlines()
    myLastUsername = lines[0].split(' :')
    myLastUsername = myLastUsername[1].strip()
    myLastPassHash = lines[1].split(' :')
    myLastPassHash = myLastPassHash[1].strip()
    myLastPassHash = pylast.md5(myLastPassHash)
    lines = []
    
print("Contacting last.fm for authentication of username: %s\n" % myLastUsername)

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = myLastUsername, password_hash = myLastPassHash)

searchedUser = input("Who are you creeping on?\n")

searchedUserNetwork = network.get_user(searchedUser)
searchedUserRecent = searchedUserNetwork.get_recent_tracks(limit=100)
searchedUserPlaylist = []

print("Fetching last.fm user: %s last 100 tracks\n" % searchedUser)

for i in range(0,len(searchedUserRecent)):
    searchedUserTrackName  = searchedUserRecent[i].track.title
    searchedUserArtistName = searchedUserRecent[i].track.artist.name
    searchedUserAlbumName  = searchedUserRecent[i].album

    searchedUserPlaylist.append((searchedUserTrackName, searchedUserArtistName, searchedUserAlbumName))

spotUsername = 'gebimble'
playlistPrefix = searchedUser + ' Last 100 - '

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')

playlistName = playlistPrefix + st

# get your token!
scope = 'playlist-modify-public'

print("Retrieving Spotify authentication token.\n")

token = util.prompt_for_user_token('gebimbe', scope=scope, client_id='a8f8d8886e3d4d51a8be009156872993', client_secret='8f0004917a7d41cf867dccd3e5c27693', redirect_uri='https://localhost:8888/callback')

print("Contacting Spotify.\n")
sp = spotipy.Spotify(auth=token)
sp.trace = False

idList = []

print("Retrieving IDs of last.fm user: %s last 100 tracks.\n" % searchedUser)

for i in range(0,len(searchedUserPlaylist)):
    trackSearchRes = sp.search(q=searchedUserPlaylist[i],type='track',limit=1)
    idList.append(trackSearchRes['tracks']['items'][0]['id'])

print("Creating playlist for Spotify user: %s, playlist name: %s,\n to accept tracks from last.fm user: %s\n" % (spotUsername,playlistName,searchedUser))

currentPlaylistData = sp.user_playlists(spotUsername)
currentPlaylistNames = []

for i in range(0,len(currentPlaylistData['items'])):
    currentPlaylistNames.append(currentPlaylistData['items'][i]['name'])
    
if playlistName in currentPlaylistNames:
    print("Playlist already exists. Think of a new name, and run again.\n")
    raise SystemExit
else:
    newPlaylist = sp.user_playlist_create(spotUsername,playlistName,public=True)
    sp.user_playlist_add_tracks(spotUsername, newPlaylist['id'], idList)
    print("Playlist created.\n\n Happy listening!")

