# simplemusicplayer
Simple MP3 Player with a statically defined text based playlist

# Overview
The purpose of writing this simple mp3 player was two fold:
1. I wanted to use wxpython which I had not used before
2. I needed to have a simple player that would play a single song in the playlist and then stop
without continuing to play the next song in the playlist. Additionally, the use case was for a shared
PC that was used for Audio/Video playback and we didn't want people playing around with the playlist.
With all the other players out there, they didn't have this 'locked down' approach in mind.

# Dependencies
vlc
wxpython

# Use
There are two variables defined at the top of the script.
SONGDIR='/tmp/mymusic/'
FILELIST='/tmp/mymusic/playlist.txt'

SONGDIR string defines the location of the mp3 files and FILELIST is the text based playlist.
The playlist is in the format of SONGNAME;FILENAME where a semi-colon is used as the delimiter.

# License
MIT LICENSE



