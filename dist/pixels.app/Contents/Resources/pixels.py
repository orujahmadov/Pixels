import subprocess
from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth   import *
import json
import urllib
import string
import random
from random import randint
import os
import time
import Tkinter
from Tkinter import *
from tkMessageBox import *

############## CONSTANT VALUES ################################################

CONSUMER_KEY = 'OSdV70a94YN4ccIg2nIgUHQQV5tiLqVY4KrkREgQ'
CONSUMER_SECRET= 'LNFCMtkbpJwW5GHoj3ezhWNsIKWALfB22SQOxQZi'
CATEGORIES_NAMES = ["Uncategorized","Abstract","Animals","Black and White","Celebrities","City and Architecture","Commercial","Concert","Family","Fashion","Film","Fine Art","Food","Journalism","Landscapes","Macro","Nature","Nude","People","Performing Arts","Sport","Still Life","Street","Transportation New!","Travel","Underwater","Urban Exploration New!","Wedding New!"]

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

DIRECTORY = os.path.expanduser("~/Desktop/500PX/")
###############################################################################

class Pixels(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        # label = Tkinter.Label(self,text="PiXeLS")
        # label.grid(column=0,row=0)

        label = Tkinter.Label(self,text="Tags")
        label.grid(column=0,row=1)
        self.entry = Tkinter.Entry(self)
        self.entry.grid(column=1,row=1,sticky='EW')

        self.category = Tkinter.StringVar()
        self.category.set('Uncategorized') #Default value

        label = Tkinter.Label(self,text="Category")
        label.grid(column=0,row=2)
        self.option = OptionMenu(self, self.category, *CATEGORIES_NAMES)
        self.option.grid(column=1,row=2)

        self.button = Tkinter.Button(self,text=u"New Wallpaper", command=self.OnButtonClick)
        self.button.grid(column=1,row=3)

        self.grid_columnconfigure(0,weight=1)

    def OnButtonClick(self):
        self.update_wallpaper(self.entry.get(), self.category.get())

    def ensure_dir_valid(self,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def set_desktop_background(self,filename):
        subprocess.Popen(SCRIPT%filename, shell=True)

    def error(self):
        showerror("Response", "Sorry, no image found with specified tags")

    def authorization_url_with_verifier(self):
        handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        token = handler.get_request_token()
        request_token = token.key
        request_token_secret = token.secret
        handler.set_request_token(request_token,request_token_secret)
        return handler

    def update_wallpaper(self, tags, category):
        handler = self.authorization_url_with_verifier()
        api = FiveHundredPXAPI(handler)
        response = json.loads(json.dumps(api.photos_search(require_auth=True, tag=tags, only=category, rpp=100, image_size=2048)))
        if len(response["photos"]) == 0:
            self.error()
        else:
            image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
            self.ensure_dir_valid(DIRECTORY)
            image_name = DIRECTORY + image_name + ".jpg"
            random_index = randint(0,len(response["photos"])-1)
            urllib.urlretrieve(response["photos"][random_index]["images"][0]["url"], image_name)
            self.set_desktop_background(image_name)


if __name__ == "__main__":
    pixels = Pixels(None)
    pixels.title('Pixels')
    pixels.mainloop()
