import yaml
from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth   import *
import os
import json
import random
import string
import urllib

############## CONSTANT VALUES ################################################
DIRECTORY = os.path.expanduser("~/Desktop/500PX/")
CONSUMER_KEY = 'OSdV70a94YN4ccIg2nIgUHQQV5tiLqVY4KrkREgQ'
CONSUMER_SECRET= 'LNFCMtkbpJwW5GHoj3ezhWNsIKWALfB22SQOxQZi'

###################### GLOBAL METHODS #########################################

def clean_directory():
	file_list = [ image_file for image_file in os.listdir(DIRECTORY)]
	for each_file in file_list:
	    os.remove(DIRECTORY+each_file)

def ensure_dir_valid():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

def get_configs():
    with open("/Users/orujahmadov/Desktop/Pixels/configs.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            return exc

def render_feature_key(feature):
    return feature.replace(" ","_").lower()


def authorization_url_with_verifier():
    handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = handler.get_request_token()
    request_token = token.key
    request_token_secret = token.secret
    handler.set_request_token(request_token,request_token_secret)
    return handler

def update_wallpaper(feature, category, interval):
    handler = authorization_url_with_verifier()
    api = FiveHundredPXAPI(handler)
    response = json.loads(json.dumps(api.photos(require_auth=True, feature=feature, only=category, rpp=100, image_size=2048)))
    if len(response["photos"]) == 0:
        error()
    else:
        ensure_dir_valid()
        clean_directory()
        for image_index in range(0,len(response["photos"])-1):
            image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
            image_name = DIRECTORY + image_name + ".jpg"
            urllib.urlretrieve(response["photos"][image_index]["images"][0]["url"], image_name)

if __name__ == "__main__":
    configs = get_configs()
    current_feature = configs["app"]["feature"]
    current_category = configs["app"]["category"]
    current_interval = configs["app"]["interval"]
    update_wallpaper(current_feature, current_category, current_interval)
