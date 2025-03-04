import requests

class Playback:
  BASE_URL = "https://api.spotify.com/v1/"
  def __init__(self,access_token):
    self.access_token = access_token
    self.headers = {"Authorization":f"Bearer {self.access_token}"}

  def search_track(self,track_name):
    url = f"{self.BASE_URL}search?q={track_name}&type=track&limit=1"
    response = requests.get(url,headers=self.headers)
    if response.status_code == 200:
        data = response.json()
        tracks = data.get("tracks", {}).get("items", [])
        if tracks:
          track_uri = tracks[0]["uri"]
          track_name = tracks[0]["name"]
          artist_name = tracks[0]["artists"][0]["name"]
          print(f"🎶 Found: {track_name} by {artist_name}")
          return track_uri
        else:
          print("❌ No track found.")
          return None
    else:
      print(f"❌ Error: {response.status_code} {response.text}")
      return None
  def play(self,song_name):
    track_uri = self.search_track(track_name=song_name)
    if not track_uri:
      return
    
    play_url = f"{self.BASE_URL}me/player/play"
    data = {"uris":[track_uri]}
    
    response = requests.put(play_url,headers=self.headers,json=data)
    if response.status_code == 204:
      print(f"🎶 Now playing: {song_name}")
    else:
      print(f"❌ Failed to play: {song_name}\nreason: {response.status_code} {response.text}")
    
