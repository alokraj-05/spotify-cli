import os
from dotenv import load_dotenv
from spotipy import SpotifyOAuth
import spotipy
import json


load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URL = os.getenv('REDIRECT_URI')
SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private playlist-modify-private playlist-modify-public"
TOKEN_PATH = ".spotify_token.json"


def login():
  auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URL,scope=SCOPE,cache_path=TOKEN_PATH,show_dialog=True)

  try:
    if os.path.exists(TOKEN_PATH):
      with open(TOKEN_PATH,"r") as file:
        token_info = json.load(file)
    else:
      token_info = auth_manager.get_access_token()
      print("Token scope",token_info.get('scope','No scope found'))
    
    if token_info is None or auth_manager.is_token_expired(token_info):
      token_info= auth_manager.refresh_access_token(token_info["refresh_token"])

    access_token = token_info["access_token"]
    sp =spotipy.Spotify(auth_manager=auth_manager)
    print("✅ Logged in successfully")
    return access_token
  except Exception as e:
    print("Error retreving access token: ",str(e))
    return None