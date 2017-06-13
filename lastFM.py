#! /usr/bin/env python


class lastFM(object):
    """
    last.fm functions
    """

    def __init__(self, user, config_file='lastRet.config'):
        self.user = user
        self.config_file = config_file

    def retrieve_API_details(self):
        """
        Retrieve last.fm API information from the file that's holding it.

        You have to have your own unique two values for API_KEY and API_SECRET
        Obtain yours from http://www.last.fm/api/account for Last.fm


        Arguments:
            API_file - API file location.

        Returns:
            API_KEY - lastFM API key
            API_SECRET - lastFM API secret
            myLastUsername - lastFM username
            myLastPassHash - lastFM password hash

        Raises:

        """
        with open(self.config_file, 'r+') as f:
            import pylast
            for line in f:
                if line.startswith('API_KEY'):
                    self.API_KEY = line.split(' : ')[1].strip()
                if line.startswith('API_SECRET'):
                    self.API_SECRET = line.split(' : ')[1].strip()
                if line.startswith('UserName'):
                    self.myLastUsername = line.split(' : ')[1].strip()
                if line.startswith('Password'):
                    myLastPassHash = line.split(' : ')[1].strip()
                    self.myLastPassHash = pylast.md5(myLastPassHash)

        return (self.API_KEY, self.API_SECRET,
                self.myLastUsername, self.myLastPassHash)

    def grab(self):
        import pylast

        self.retrieve_API_details()

        network = pylast.LastFMNetwork(api_key=self.API_KEY,
                                       api_secret=self.API_SECRET,
                                       username=self.myLastUsername,
                                       password_hash=self.myLastPassHash)

        searchedUserNetwork = network.get_user(self.user)
        searchedUserRecent = searchedUserNetwork.get_recent_tracks(limit=100)

        self.userPlaylist = {}

        i = 1

        for item in searchedUserRecent:
            trackPos = 'track' + str(i)
            title = item.track.title
            artist = item.track.artist.name
            album = item.album
            self.userPlaylist[trackPos] = {'title': title,
                                           'artist': artist,
                                           'album': album}

            i = i + 1

        return self.userPlaylist

    def dict2list(self):
        """
        Turns the userPlaylist dictionary into a list.
        """

        self.userPlaylistList = []

        for track in self.userPlaylist:
            trackString = ' - '.join([self.userPlaylist[track][val] for val in
                                      self.userPlaylist[track]])

            self.userPlaylistList.append(trackString)

        return self.userPlaylistList
