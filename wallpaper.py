import subprocess
from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth   import *
import json
import urllib
import string
import random
from random import randint
import os
import schedule
import time
import Tkinter

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

class Pixels(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry = Tkinter.Entry(self)
        self.entryVariable.set(u"Enter tags here")
        self.entry.grid(column=0,row=0,sticky='EW')

        button = Tkinter.Button(self,text=u"New Wallpaper", command=self.OnButtonClick)
        button.grid(column=0,row=1)

        self.grid_columnconfigure(0,weight=1)

    def OnButtonClick(self):
        self.update_wallpaper(self.entry.get())

    def set_desktop_background(self,filename):
        subprocess.Popen(SCRIPT%filename, shell=True)

    def authorization_url_with_verifier(self):
        CONSUMER_KEY = 'OSdV70a94YN4ccIg2nIgUHQQV5tiLqVY4KrkREgQ'
        CONSUMER_SECRET= 'LNFCMtkbpJwW5GHoj3ezhWNsIKWALfB22SQOxQZi'
        handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        token = handler.get_request_token()
        request_token = token.key
        request_token_secret = token.secret
        handler.set_request_token(request_token,request_token_secret)
        return handler

    def update_wallpaper(self, tags):
        handler = self.authorization_url_with_verifier()
        api = FiveHundredPXAPI(handler)
        response = json.loads(json.dumps(api.photos_search(require_auth=True, tag=tags, rpp=100, image_size=2048)))
        image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        image_name = os.path.expanduser("~/Desktop/500PX/") + image_name + ".jpg"
        random_index = randint(0,len(response["photos"]))
        urllib.urlretrieve(response["photos"][random_index]["images"][0]["url"], image_name)
        self.set_desktop_background(image_name)


# schedule.every(1).minutes.do(update_wallpaper)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

if __name__ == "__main__":
    pixels = Pixels(None)
    pixels.title('Pixels')
    pixels.mainloop()
