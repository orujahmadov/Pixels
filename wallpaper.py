import subprocess
from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth   import *
import json
import urllib
import string
import random
from random import randint

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

def authorization_url_with_verifier():
    CONSUMER_KEY = 'OSdV70a94YN4ccIg2nIgUHQQV5tiLqVY4KrkREgQ'
    CONSUMER_SECRET= 'LNFCMtkbpJwW5GHoj3ezhWNsIKWALfB22SQOxQZi'
    handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = handler.get_request_token()
    request_token = token.key
    request_token_secret = token.secret
    handler.set_request_token(request_token,request_token_secret)
    return handler

handler = authorization_url_with_verifier()
api = FiveHundredPXAPI(handler)
response = json.loads(json.dumps(api.photos(require_auth=True, feature='popular',only="City and Architecture", rpp=100, image_size=2048)))
image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
image_name = "/Users/orujahmadov/Desktop/500PX/" + image_name + ".jpg"
random_index = randint(0,99)
urllib.urlretrieve(response["photos"][random_index]["images"][0]["url"], image_name)
set_desktop_background(image_name)
