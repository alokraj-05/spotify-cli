from Scripts.Playback import Playback

class Playlist:
    BASE_URL = "https://api.spotify.com/v1/"
    def __init__(self, access_token,sp):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.playback = Playback(self.access_token)
        self.user_id = self.playback.get_user_id()
        self.sp = sp
    
    def get_playlist_id(self, playlist_name):
      user_id = self.user_id
      playlists = self.sp.user_playlists(user_id)
      while playlists:
        for i, playlist in enumerate(playlists['items']):
          if(playlist['name'].lower() == playlist_name.lower()):
             return playlist['id']
        if playlists['next']:
          playlists = self.sp.next(playlists)
        else:
          playlists = None
          return None
    
    def get_playlist(self, playlist_name):
      id = self.get_playlist_id(playlist_name)
      playlist = self.sp.user_playlist(id);
      if(playlist):
         return playlist
      else:
         return None

    def add_songs(self,data):
      lst_data = list(data)
      if len(lst_data) < 2:
         print("Provide at least 1 song with playlist name")
         return
      playlist_name = lst_data[-1]
      playlist_id = self.get_playlist_id(playlist_name)
      if playlist_id == None:
        new_playlist = self.sp.user_playlist_create(self.user_id,playlist_name)
        print(f"Created new playlist: {new_playlist['name']}")
      best_matched_songs = []
      for idx in range(0,len(lst_data)-1):
          intended_song = self.playback.search_track(lst_data[idx])
          best_matched_songs.append(intended_song)
          print(f'✅ Added song {intended_song} in playlist {playlist_name}')
      res = self.sp.playlist_add_items(playlist_id,best_matched_songs)
      return res
    
    def get_all_playlists(self):
      user_id = self.user_id
      playlists = self.sp.user_playlists(user_id)

      return playlists["items"]

           

