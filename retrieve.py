#! /usr/bin/env python

from lastFM import lastFM
from spotify import spotify

import pprint

pp = pprint.PrettyPrinter()

grabbedUser = 'thruttle'

grabbed = lastFM(grabbedUser)
grabbed.grab()
grabbed_playlist = grabbed.dict2list()

spot = spotify(grabbed_playlist, grabbedUser)
spot.playlist_make()
