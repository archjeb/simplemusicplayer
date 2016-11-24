#!/usr/bin/env python
'''
simplemusicplayer.py

Simplemusicplayer is just that, a simple MP3 player that uses a static playlist.
The purpose of writing this program is to provide a simple player that plays only
a single seleted song in the playlist and then stops without proceeding to the next
song in the playlist. Additionally, the use case was a shared computer and we didn't want
people accidently deleting songs in the playlist.

simplemusicplayer has the following dependencies:

wxpython
vlc

A playlist file is needed in the following format:
Song Title;filename.mp3

Where song title is just an alphanumeric string and the filename is an mp3 file
and a semi-colon is used as a delimiter.

The variables below allow you to customize the directory of where your MP3s are located
and you can customize the location and name of the playlist file.
'''

#***********************************************************************
# Version 0.1  - 11/23/2016 - Initial Version - Jeremy Georges
#
#***********************************************************************


###################
#Global Variables #
###################
SONGDIR='/tmp/music/'
FILELIST='/tmp/music/playlist.txt'


###########
# MODULES #
###########
import sys
import wx
import vlc


class MainMenu(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(350, 350))

        #Create menubar object
        menubar = wx.MenuBar()
        #add menus
        file = wx.Menu()
        help = wx.Menu()

        #add items under menu
        file.Append(101, '&Play', 'Play Song')
        file.Append(102, '&Stop', 'Stop Song')

        #Add a separator
        file.AppendSeparator()
        quit = wx.MenuItem(file,105, '&Quit\tCtrl+Q', 'Quit the Application')
        file.AppendItem(quit)
        menubar.Append(file, '&File')
        menubar.Append(help, '&Help')
        help.Append(200, '&About', 'About Simple Player')

        #panel handle
        panel = wx.Panel(self, -1)

        #create sizers, 1 for buttons and 1 for the Boxlist
        topsizer= wx.BoxSizer(wx.HORIZONTAL)
        self.playbtn = wx.Button(panel, -1, "Play", (0,0))
        self.stopbtn = wx.Button(panel, -1, "Stop", (80,0))

        #Add these buttons to the sizer window
        topsizer.Add(self.playbtn,0)
        topsizer.Add(self.stopbtn,0)

        #Setup sizer for the Ctrllist, we'll add to it later
        bottomsizer = wx.BoxSizer(wx.VERTICAL)

        self.SetMenuBar(menubar)
        self.Centre()

        self.CreateStatusBar()
        #Bind our menu items to functions
        self.Bind(wx.EVT_MENU, self.onQuit, id=105)
        self.Bind(wx.EVT_MENU, self.onAboutDlg, id=200)
        self.Bind(wx.EVT_MENU, self.onClickPlay, id=101)
        self.Bind(wx.EVT_MENU, self.onClickStop, id=102)

        #Lets setup our list of songs
        #Index will be used as we iterate through the playlist
        #The SongDict will be indexed list of the songs associated with their index
        #into our ListBox. So the index of the Listbox will be the dictionary key to
        #each song in the playlist.

        self.index = 0
        self.SongDict={}
        #Index to file in playlist of current song. We need this as a pointer to the dictionary key.
        self.CurrentSongSelected='0'

        self.list_box = wx.ListBox(panel, pos = (0, 100),size = (100, -1), style = wx.LB_SINGLE | wx.LB_NEEDED_SB)
        bottomsizer.Add(self.list_box, 0, flag=wx.EXPAND|wx.TOP, border=50)
        panel.SetSizer(topsizer)
        panel.SetSizer(bottomsizer)

        #Add the list of songs
        self.add_song_list()

        #Bind our selection event to our function to handler
        self.Bind(wx.EVT_LISTBOX, self.onListBox, self.list_box)
        #We could just do a single function and then use event.GetEventObject().GetLabel()
        #to get the label of the button pushed. But lets keep play and stop in separate
        #functions for now. I think it will be easier to read the code that way.
        self.playbtn.Bind(wx.EVT_BUTTON, self.onClickPlay)
        self.stopbtn.Bind(wx.EVT_BUTTON, self.onClickStop)

        #Setup our vlc bindings
        self.instance = vlc.Instance()

        #Create a MediaPlayer with the default instance
        self.player = self.instance.media_player_new()


    def add_song_list(self):
        try:
            with open(FILELIST) as fh:
               for line in fh:
                   songlist=line.rstrip('\n').split(';')
                   theindex = "%s" % self.index
                   self.SongDict[theindex]=songlist
                   #need to append the song title to our ListBox
                   self.list_box.Append(str(songlist[0]))
                   self.index += 1
        except:
            print "Error reading playlist file %s" % FILELIST
            sys.exit(1)

    def onListBox(self, event):
        #Set CurrentSongSelected to the index of the song
        self.CurrentSongSelected=str(event.GetEventObject().GetSelection())

    def onClickPlay(self,event):
        #Load the media file
        FULLSONGPATH=SONGDIR+self.SongDict[(self.CurrentSongSelected)][1]
        media = self.instance.media_new(FULLSONGPATH)
        self.player.set_media(media)
        self.player.audio_set_volume(100)
        self.player.play()

    def onClickStop(self,event):
        self.player.stop()

    def onQuit(self, event):
        dlg = wx.MessageDialog(self, "Do you really want to close this application?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Close()


    #Builtin Method for about box
    def onAboutDlg(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Simple MP3 Player"
        info.Version = "0.1 Beta"
        info.Copyright = "(C) 2016 Jeremy Georges"
        info.Description = "Simple MP3 Player to use a static playlist of songs"
        info.WebSite = ("https://github.com/archjeb", "My Home GitHub Page")
        info.Developers = ["Jeremy Georges"]
        licenseText = '''
MIT License

Copyright (c) [2016] [Jeremy Georges]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
        info.License = (licenseText)
        # Show the wx.AboutBox
        wx.AboutBox(info)

class MusicPlayerApp(wx.App):
    def OnInit(self):
        frame = MainMenu(None, -1, 'Simple Music Player')
        frame.Show(True)
        frame.Centre()
        return True




#=============================================
# MAIN
#=========================================================

def main():
    # Create App object
    app = MusicPlayerApp(0)
    app.MainLoop()




if __name__ == "__main__":
    main()
