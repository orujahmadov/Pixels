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
CATEGORY_NAMES = ["Uncategorized","Abstract","Animals","Black and White","Celebrities","City and Architecture","Commercial","Concert","Family","Fashion","Film","Fine Art","Food","Journalism","Landscapes","Macro","Nature","Nude","People","Performing Arts","Sport","Still Life","Street","Transportation New!","Travel","Underwater","Urban Exploration New!","Wedding New!"]
FEATURE_NAMES = ["Popular","Upcoming","Fresh Today","Fresh Yesterday","Fresh Week"]

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

        self.feature = Tkinter.StringVar()
        self.feature.set('Popular') #Default value

        label_feature = Tkinter.Label(self,text="Feature")
        label_feature.grid(column=0,row=1)
        self.option_feature = OptionMenu(self, self.feature, *FEATURE_NAMES)
        self.option_feature.grid(column=1,row=1)

        self.category = Tkinter.StringVar()
        self.category.set('Uncategorized') #Default value

        label_category = Tkinter.Label(self,text="Category")
        label_category.grid(column=0,row=2)
        self.option_category = OptionMenu(self, self.category, *CATEGORY_NAMES)
        self.option_category.grid(column=1,row=2)

        self.button = Tkinter.Button(self,text=u"New Wallpaper", command=self.OnButtonClick)
        self.button.grid(column=1,row=3)

        self.grid_columnconfigure(0,weight=1)

    def OnButtonClick(self):
        selected_feature = self.feature.get().replace(" ","_").lower()
        selected_category = self.category.get()
        self.update_wallpaper(selected_feature, selected_category)

    def ensure_dir_valid(self,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def set_desktop_background(self,filename):
        subprocess.Popen(SCRIPT%filename, shell=True)

    def error(self):
        showerror("Response", "Sorry, no image found with specified options")

    def authorization_url_with_verifier(self):
        handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        token = handler.get_request_token()
        request_token = token.key
        request_token_secret = token.secret
        handler.set_request_token(request_token,request_token_secret)
        return handler

    def update_wallpaper(self, feature, category):
        handler = self.authorization_url_with_verifier()
        api = FiveHundredPXAPI(handler)
        response = json.loads(json.dumps(api.photos(require_auth=True, feature=feature, only=category, rpp=100, image_size=2048)))
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
