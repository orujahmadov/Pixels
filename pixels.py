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
import ttk
import yaml

############## CONSTANT VALUES ################################################
DIRECTORY = os.path.expanduser("~/Desktop/500PX/")
CONSUMER_KEY = 'OSdV70a94YN4ccIg2nIgUHQQV5tiLqVY4KrkREgQ'
CONSUMER_SECRET= 'LNFCMtkbpJwW5GHoj3ezhWNsIKWALfB22SQOxQZi'
CATEGORY_NAMES = ["Uncategorized","Abstract","Animals","Black and White","Celebrities","City and Architecture","Commercial","Concert","Family","Fashion","Film","Fine Art","Food","Journalism","Landscapes","Macro","Nature","Nude","People","Performing Arts","Sport","Still Life","Street","Transportation New!","Travel","Underwater","Urban Exploration New!","Wedding New!"]
FEATURE_NAMES = ["Popular","Editors","Upcoming","Fresh Today","Fresh Yesterday","Fresh Week"]
INTERVAL_NAMES = ["Every 5 seconds","Every minute","Every 5 minutes","Every 15 minutes","Every 30 minutes","Every hour","Every day"]

############### DICTIONARIES #################################################
INTERVAL_DICTIONARY = {"Every 5 seconds":5.0, "Every minute":60.0, "Every 5 minutes":300.0, "Every 15 minutes":900.0, "Every 30 minutes":1800.0, "Every hour":3600.0, "Every day":86400.0}
INTERVAL_DICTIONARY_REVERSE = {"5.0":"Every 5 seconds", "60.0":"Every minute", "300.0":"Every 5 minutes", "900.0":"Every 15 minutes", "1800.0":"Every 30 minutes", "3600.0":"Every hour", "86400.0":"Every day"}

SCRIPT = """/usr/bin/osascript<<END
tell application "System Events"
	tell current desktop
		set pictures folder to {}
		set change interval to {}
		set random order to true
	end tell
end tell
END"""

SCRIPT_INTERVAL = """/usr/bin/osascript<<END
tell application "System Events"
	tell current desktop
		set change interval to {}
	end tell
end tell
END"""
###############################################################################

###################### GLOBAL METHODS #########################################
def clean_directory():
	file_list = [ image_file for image_file in os.listdir(DIRECTORY)]
	for each_file in file_list:
	    os.remove(DIRECTORY+each_file)

def ensure_dir_valid():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

def get_configs():
    with open("configs.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            return exc

def update_configs(data):
    with open('configs.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=True)

def render_feature_key(feature):
    return feature.replace(" ","_").lower()

###############################################################################

class Pixels(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        self.configs = get_configs()
        #### Global Variables
        self.response = ""
        self.current_feature = self.configs["app"]["feature"]
        self.current_category = self.configs["app"]["category"]
        self.current_interval = self.configs["app"]["interval"]

		####### UI ###########################

		# FEATURE
        self.feature = Tkinter.StringVar()
        feature_select = self.current_feature if self.current_feature is not None else "Popular"
        self.feature.set(feature_select) #Default value

        label_feature = Tkinter.Label(self,text="Feature")
        label_feature.grid(column=0,row=1,sticky=E)
        self.option_feature = OptionMenu(self, self.feature, *FEATURE_NAMES)
        self.option_feature.grid(column=1,row=1,sticky=EW, padx=5, pady=5)

        self.category = Tkinter.StringVar()
        category_select = self.current_category if self.current_category is not None else "Uncategorized"
        self.category.set(category_select) #Default value

		# CATEGORY
        label_category = Tkinter.Label(self,text="Category")
        label_category.grid(column=0,row=2,sticky=E)
        self.option_category = OptionMenu(self, self.category, *CATEGORY_NAMES)
        self.option_category.grid(column=1,row=2,sticky=EW, padx=5, pady=5)

		# INTERVAL
        self.interval = Tkinter.StringVar()
        interval_select = INTERVAL_DICTIONARY_REVERSE[str(self.current_interval)] if self.current_interval is not None else "Every hour"
        self.interval.set(interval_select) #Default value

        label_interval = Tkinter.Label(self,text="Interval")
        label_interval.grid(column=0,row=3,sticky=E)
        self.option_interval = OptionMenu(self, self.interval, *INTERVAL_NAMES)
        self.option_interval.grid(column=1,row=3,sticky=EW, padx=5, pady=5)

        self.button = Tkinter.Button(self,text=u"Save Changes", command=self.OnSaveClick)
        self.button.grid(column=1,row=4,sticky=EW, padx=5, pady=5)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.image_index = 0
        self.image_max_index = 100
        self.progress.grid(column=1,row=5,sticky=EW, padx=5, pady=10)

    def OnSaveClick(self):
        selected_feature = self.feature.get()
        selected_category = self.category.get()
        selected_interval = INTERVAL_DICTIONARY[self.interval.get()]
		# Update YAML config filename
        self.configs["app"]["feature"] = selected_feature
        self.configs["app"]["category"] = selected_category
        self.configs["app"]["interval"] = selected_interval
        update_configs(self.configs)
        self.update_wallpaper(render_feature_key(selected_feature), selected_category, selected_interval)

    def set_desktop_background(self,filename, interval):
		subprocess.Popen(SCRIPT.format('"'+DIRECTORY+'"', interval), shell=True)

    def error(self):
        showerror("Response", "Sorry, no image found with specified options")

    def authorization_url_with_verifier(self):
        handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        token = handler.get_request_token()
        request_token = token.key
        request_token_secret = token.secret
        handler.set_request_token(request_token,request_token_secret)
        return handler

    def update_wallpaper(self, feature, category, interval):
        handler = self.authorization_url_with_verifier()
        api = FiveHundredPXAPI(handler)
        self.response = json.loads(json.dumps(api.photos(require_auth=True, feature=feature, only=category, rpp=100, image_size=2048)))
        if len(self.response["photos"]) == 0:
            self.error()
        else:
            ensure_dir_valid()
            clean_directory()
            image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
            image_name = DIRECTORY + image_name + ".jpg"
            urllib.urlretrieve(self.response["photos"][0]["images"][0]["url"], image_name)
            self.set_desktop_background(image_name, interval)
            self.image_index = 0
            self.progress["value"] = 0
            self.progress["maximum"] = 100
            self.download_images()

    def download_images(self):
        self.image_index += 1
        self.progress["value"] = self.image_index
        if self.image_index < self.image_max_index:
            image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
            image_name = DIRECTORY + image_name + ".jpg"
            urllib.urlretrieve(self.response["photos"][self.image_index]["images"][0]["url"], image_name)
            self.after(100, self.download_images)


if __name__ == "__main__":
    pixels = Pixels(None)
    pixels.title('Pixels')
    pixels.resizable(width=False, height=False)
    pixels.mainloop()
