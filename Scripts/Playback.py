import requests
from filter.fuzzySearch import fuzzy_search
import os
import time
import webbrowser
from filter.runApp import findNdLaunch

class Playback:
  BASE_URL = "https://api.spotify.com/v1/"
  def __init__(self,access_token):
    self.access_token = access_token
    self.headers = {"Authorization":f"Bearer {self.access_token}"}
    self.user_id = self.get_user_id()

  def get_user_id(self):
    url = f"{self.BASE_URL}me"
    response = requests.get(url, headers=self.headers)
    if response.status_code == 200:
      return response.json()['id']
    else:
      print(f"❌ failed to get user ID: {response.status_code} {response.text}")


  def search_track(self,track_name, use_fuzzy=True, search_limit=50):
    """
    Search Spotify and optionally apply fuzzy matching across the returned items.
    Returns the chosen track URI or None.
    """
    url = f"{self.BASE_URL}search?q={track_name}&type=track&limit={search_limit}"
    response = requests.get(url,headers=self.headers)
    if response.status_code == 200:
        data = response.json()
        tracks = data.get("tracks", {}).get("items", [])
        if not tracks:
          print("❌ No track found.")
          return None

        if use_fuzzy and len(tracks) > 1:
          matches = fuzzy_search(tracks, track_name, top_n=1)
          if matches:
            best = matches[0]
            track_uri = best.get("uri")
            print(f"🎶 Found (fuzzy): {best.get('name')} by {best.get('artist')} "
                  f"(pop:{best.get('popularity')} score:{best.get('score')} substr:{best.get('substring')})")
            return track_uri
          else:
            # fallback to first item if fuzzy didn't return anything
            chosen = tracks[0]
            track_uri = chosen.get("uri")
            track_name = chosen.get("name")
            artist_name = chosen.get("artists", [{}])[0].get("name", "")
            print(f"🎶 Found: {track_name} by {artist_name}")
            return track_uri
        else:
          # use the top search result directly
          track = tracks[0]
          track_uri = track.get("uri")
          track_name = track.get("name")
          artist_name = track.get("artists", [{}])[0].get("name", "")
          print(f"🎶 Found: {track_name} by {artist_name}")
          return track_uri
    else:
      print(f"❌ Error: {response.status_code} {response.text}")
      return None
    

  def _open_spotify_app_and_play(self, track_uri):
    """Try to open the desktop Spotify client and play the given spotify: URI."""
    try:
      # Prefer OS-native open on Windows
      if os.name == 'nt':
        try:
          os.startfile(track_uri)  # will open registered spotify: handler
        except Exception:
          webbrowser.open(track_uri)
      else:
        webbrowser.open(track_uri)

      # Also attempt to launch the Spotify exe if present
      try:
        findNdLaunch("Spotify")
      except Exception:
        pass

      return True
    except Exception as e:
      print(f"❌ Failed to launch Spotify app: {e}")
      return False

  def play(self,song_name):
    self.song_name = song_name
    track_uri = self.search_track(track_name=song_name)
    if not track_uri:
      return

    self.play_url = f"{self.BASE_URL}me/player/play"
    data = {"uris":[track_uri]}

    response = requests.put(self.play_url,headers=self.headers,json=data)
    # Success
    if response.status_code == 204:
      return response

    # If playback failed, check for "device not found" or similar and try opening app
    msg = ""
    try:
      resp_json = response.json()
      msg = resp_json.get('error', {}).get('message', '') or str(resp_json)
    except Exception:
      msg = response.text or ""

    if response.status_code == 404 or 'device' in msg.lower():
      print("⚠️ No active Spotify device found. Attempting to open native Spotify app and play directly...")
      opened = self._open_spotify_app_and_play(track_uri)
      if opened:
        # give the app a moment to register as an active device
        time.sleep(3)
        response = requests.put(self.play_url,headers=self.headers,json=data)
        if response.status_code == 204:
          print("✅ Playback started after launching Spotify app.")
          return response
        else:
          print(f"❌ Still failed to start playback after launching app: {response.status_code} {response.text}")
          return response
      else:
        print("❌ Could not open Spotify app to start playback.")
        return response

    # Other errors
    print(f"❌ Error: {response.status_code} {response.text}")
    return response
    
  def pause(self):
    pause_url = f"{self.BASE_URL}me/player/pause"
    response = requests.put(pause_url,headers=self.headers)
    if response.status_code == 204:
      print(f"⏸️ Paused {self.song_name}")
    else:
      print(f"Error: {response.status_code} {response.text}")
  
  
  def get_playlist(self,playlist_url):
    playlist_id = playlist_url.split("/")[4].split("?")[0]
    url = f"{self.BASE_URL}playlists/{playlist_id}"
    response = requests.get(url,headers=self.headers)
    if response.status_code == 200:
      data = response.json()
      tracks = data.get('tracks')["items"]
      for track_id in tracks:
        items = tracks[0]
        track_id = items.get("track").get("album")['id']
        
      total = data.get("tracks")['total']
      followers = data.get("followers")['total']
      display_name = data.get("owner")['display_name']
      playlist_name = data.get("name")
      id = data.get("id")
      is_public = data.get("public")

      print(f"📃 Playlist: {playlist_name}\n📛 Owner: {display_name}\n➡️ Total Followers: {followers}\n🈁 Total Items: {total}\n🆔 ID: {id}\n📢 is Public : {is_public}")
    return playlist_id
    

  def play_playlist(self,url):
    track_id = self.get_playlist(url)
    if not track_id:
      return
    self.play_url = f"{self.BASE_URL}me/player/play"
    data = {"context_uri":f"spotify:playlist:{track_id}"}
    response = requests.put(self.play_url,headers=self.headers,json=data)
    if response.status_code == 204:
      print(f"📃 Playlist added to Spotify queue.")
    else:
      print(f"❌ Error: {response.status_code} {response.text}")

# Merge two playlists program 
  def get_plalist_deatils(self,playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    url = f"{self.BASE_URL}playlists/{playlist_id}"

    response = requests.get(url,headers=self.headers)
    if response.status_code == 200:
      data = response.json()
      return {
        "id": playlist_id,
        "name":data['name'],
        "owner":data['owner']['display_name'],
        "track_count": len(data['tracks']['items']),
        "track_uris":[track['track']['uri'] for track in data['tracks']['items'] if track['track']]
      }
    else:
      print(f"❌ Error fetching playlist details: {response.status_code} {response.text}")
      return None
  def create_new_playlist(self, new_playlist_name):
    if not self.user_id:
      print("❌ User ID not found. Cannot create playlist.")
      return None
    
    url = f"{self.BASE_URL}users/{self.user_id}/playlists"
    data = {"name":new_playlist_name,"public":False,"description":"New Playlist"}

    response = requests.post(url,headers={"Authorization":f"Bearer {self.access_token}","Content-type":"application/json"},json=data)
    if response.status_code == 201:
      return response.json()['id']
    else:
      print(f"❌ Error creating new playlist: {response.status_code} {response.text}")
  
  def merge_playlist(self,new_playlist_name,playlist1_url,playlist2_url):
    playlist1 = self.get_plalist_deatils(playlist1_url)
    playlist2 = self.get_plalist_deatils(playlist2_url)

    if not playlist1 or not playlist2:
      print("❌ Could not fetch both playlists.")
      return
    
    print(f"\n🎵 **Merging Playlists:**\n"
    f"1️⃣ {playlist1['name']} by {playlist1['owner']} ({playlist1['track_count']} tracks)\n"
    f"2️⃣ {playlist2['name']} by {playlist2['owner']} ({playlist2['track_count']} tracks)")

    new_playlist_id = self.create_new_playlist(new_playlist_name)
    if not new_playlist_id:
      return
    
    track_uris = list(set(playlist1['track_uris']+playlist2['track_uris']))
    add_url = f"{self.BASE_URL}playlists/{new_playlist_id}/tracks"
    response = requests.post(add_url,headers=self.headers,json={'uris':track_uris})

    if response.status_code == 201:
      print(f"✅ New Playlist Created: '{new_playlist_name}' ({len(track_uris)} tracks)")
    else:
      print(f"❌ Error adding tracks: {response.status_code} {response.text}")