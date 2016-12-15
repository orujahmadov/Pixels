import subprocess
from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth   import *
import json
import urllib
import string
import random
from random import randint
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import unirest
# Just importing Forsimatic class
from forismatic import Forismatic
from AppKit import NSScreen

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)

def authorization_url_with_verifier():
    CONSUMER_KEY = 'OSdV70a94YN4ccIg2nIgUHQQV5tiLqVY4KrkREgQ'
    CONSUMER_SECRET= 'LNFCMtkbpJwW5GHoj3ezhWNsIKWALfB22SQOxQZi'
    handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = handler.get_request_token()
    request_token = token.key
    request_token_secret = token.secret
    handler.set_request_token(request_token,request_token_secret)
    return handler

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

handler = authorization_url_with_verifier()
api = FiveHundredPXAPI(handler)
response = json.loads(json.dumps(api.photos_search(require_auth=True, tag="city sunrise", rpp=100, image_size=2048)))
image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
image_name = "/Users/orujahmadov/Desktop/500PX/" + image_name + ".jpg"
random_index = randint(0,len(response["photos"]))
urllib.urlretrieve(response["photos"][random_index]["images"][0]["url"], image_name)
set_desktop_background(image_name)

font = ImageFont.truetype("/Users/orujahmadov/Downloads/open_sans/OpenSans-Regular.ttf", 35)
img = Image.open(image_name)
draw = ImageDraw.Draw(img)
forismatic = Forismatic()
quotes = forismatic.get_quote()
W, H = (800,1200)
w, h = draw.textsize(quotes.quote)
draw.text(((W-w)/2,(H-h)/2), "\"" + quotes.quote + "\"", (250,250,250), font=font)
img.save("/Users/orujahmadov/Desktop/test.jpg")
print(NSScreen.mainScreen().frame().size.width)
print(NSScreen.mainScreen().frame().size.height)
