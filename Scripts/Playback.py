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
    self.song_name = song_name
    track_uri = self.search_track(track_name=song_name)
    if not track_uri:
      return
    
    self.play_url = f"{self.BASE_URL}me/player/play"
    data = {"uris":[track_uri]}
    
    response = requests.put(self.play_url,headers=self.headers,json=data)
    if response.status_code == 204:
      print(f"🎶 Now playing: {song_name}")
    else:
      print(f"❌ Failed to play: {song_name}\nreason: {response.status_code} {response.text}")
    
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
        print(track_id)
        return track_id
    

  def play_playlist(self,url):
    track_id = self.get_playlist(url)
    if not track_id:
      return
    
    self.play_url = f"{self.BASE_URL}me/player/play"
    data = {"context_uri":f"spotify:album:{track_id}"}
    response = requests.put(self.play_url,headers=self.headers,json=data)
    if response.status_code == 204:
      print(f"📃 Playlist added to Spotify queue.")
    else:
      print(f"❌ Error: {response.status_code} {response.text}")

