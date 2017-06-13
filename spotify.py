#! /usr/bin/env python


class spotify(object):

    def __init__(self,
                 userPlaylist,
                 grabbedUser,
                 user='gebimble',
                 config_file='lastRet.config'):

        import time
        import datetime

        self.user = user
        self.grabbedUser = grabbedUser

        playlistPrefix = self.grabbedUser + ' Last 100 - '
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
        self.playlistName = playlistPrefix + st

        self.config_file = config_file
        self.userPlaylist = userPlaylist

    def SPOTIFYAPIgrabber(self):
        """
        Retrieve spotify API information from the file that's holding it.

        You have to have your own unique two values for API_KEY and API_SECRET
        Obtain yours from the good folks at spotify


        Arguments:
            config_file - API file location.

        Returns:
            SPOTIPY_CLIENT_ID - user name
            SPOTIPY_CLIENT_SECRET - response to secret question
            SPOT_REDIRECT_URI - redirect url

        Raises:

        """
        with open(self.config_file, 'r+') as f:
            for line in f:
                if line.startswith('SPOTIPY_CLIENT_ID'):
                    self.SPOTIPY_CLIENT_ID = line.split(' : ')[1].strip()
                if line.startswith('SPOTIPY_CLIENT_SECRET'):
                    self.SPOTIPY_CLIENT_SECRET = line.split(' : ')[1].strip()
                if line.startswith('SPOTIPY_REDIRECT_URI'):
                    self.SPOTIPY_REDIRECT_URI = line.split(' : ')[1].strip()

            return (self.SPOTIPY_CLIENT_ID, self.SPOTIPY_CLIENT_SECRET,
                    self.SPOTIPY_REDIRECT_URI)

    def get_token(self):

        import spotipy.util as util

        self.SPOTIFYAPIgrabber()

        user = 'gebimble'
        scope = 'playlist-modify-public playlist-modify-private'
        id_val = self.SPOTIPY_CLIENT_ID
        secret_val = self.SPOTIPY_CLIENT_SECRET
        uri_val = self.SPOTIPY_REDIRECT_URI

        self.token = util.prompt_for_user_token(user,
                                                scope=scope,
                                                client_id=id_val,
                                                client_secret=secret_val,
                                                redirect_uri=uri_val)

        return self.token

    def playlist_make(self):

        import spotipy

        self.get_token()

        sp = spotipy.Spotify(auth=self.token)

        sp.trace = False

        idList = []

        for track in self.userPlaylist:
            result = sp.search(q=track, type='track', limit=1)
            if result['tracks']['items']:
                idList.append(result['tracks']['items'][0]['id'])

        new_playlist = sp.user_playlist_create(self.user,
                                               self.playlistName,
                                               public=True)

        sp.user_playlist_add_tracks(self.user, new_playlist['id'], idList)
