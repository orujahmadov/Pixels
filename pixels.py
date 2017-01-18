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
FEATURE_NAMES = ["Popular","Editors","Upcoming","Fresh Today","Fresh Yesterday","Fresh Week"]
INTERVAL_NAMES = ["Every 5 seconds","Every minute","Every 5 minutes ","Every 15 minutes","Every 30 minutes","Every hour","Every day"]

############### DICTIONARIES #################################################
INTERVAL_DICTIONARY = {"Every 5 seconds":5.0, "Every minute":60.0, "Every 5 minutes":300.0, "Every 15 minutes":900.0, "Every 30 minutes":1800, "Every hour":3600.0, "Every day":86400.0}

SCRIPT = """/usr/bin/osascript<<END
tell application "System Events"
	tell current desktop
		set pictures folder to "/Users/orujahmadov/Desktop/500PX"
		set change interval to {}
		set random order to true
	end tell
end tell
END"""

DIRECTORY = os.path.expanduser("~/Desktop/500PX/")
###############################################################################

###################### GLOBAL METHODS #########################################
def clean_directory():
	file_list = [ image_file for image_file in os.listdir(DIRECTORY)]
	for each_file in file_list:
	    os.remove(DIRECTORY+each_file)

def ensure_dir_valid():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

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
        label_feature.grid(column=0,row=1,sticky=E)
        self.option_feature = OptionMenu(self, self.feature, *FEATURE_NAMES)
        self.option_feature.grid(column=1,row=1,sticky=W)

        self.category = Tkinter.StringVar()
        self.category.set('Uncategorized') #Default value

        label_category = Tkinter.Label(self,text="Category")
        label_category.grid(column=0,row=2,sticky=E)
        self.option_category = OptionMenu(self, self.category, *CATEGORY_NAMES)
        self.option_category.grid(column=1,row=2,sticky=W)

        self.interval = Tkinter.StringVar()
        self.interval.set('Every hour') #Default value

        label_interval = Tkinter.Label(self,text="Interval")
        label_interval.grid(column=0,row=3,sticky=E)
        self.option_interval = OptionMenu(self, self.interval, *INTERVAL_NAMES)
        self.option_interval.grid(column=1,row=3,sticky=W)

        self.button = Tkinter.Button(self,text=u"New Wallpaper", command=self.OnButtonClick)
        self.button.grid(column=1,row=4,sticky=W)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

    def OnButtonClick(self):
        selected_feature = self.feature.get().replace(" ","_").lower()
        selected_category = self.category.get()
        self.update_wallpaper(selected_feature, selected_category)

    def set_desktop_background(self,filename):
		subprocess.Popen(SCRIPT.format(INTERVAL_DICTIONARY[self.interval.get()]), shell=True)

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
            ensure_dir_valid()
            clean_directory()
            image_name = ""
            for index in range(len(response["photos"])-1):
                image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
                image_name = DIRECTORY + image_name + ".jpg"
                urllib.urlretrieve(response["photos"][index]["images"][0]["url"], image_name)
            self.set_desktop_background(image_name)


if __name__ == "__main__":
    pixels = Pixels(None)
    pixels.title('Pixels')
    pixels.mainloop()
