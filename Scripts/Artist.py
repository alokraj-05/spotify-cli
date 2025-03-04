import requests
class Artist:
  BASE_URL = "https://api.spotify.com/v1/"
  def __init__(self,access_token):
    self.access_token = access_token


  def artist_name(self,name):
    url = f"{self.BASE_URL}search?q={name}&type=artist&limit=5"
    headers = {"Authorization":f"Bearer {self.access_token}"}
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
      data = response.json()
      artists = data.get("artists",{}).get("items",[])
      if artists:
        print("\n🔍 Search Results:")
        for artist in artists:
          name = artist['name']
          popularity = artist['popularity']
          uri = artist['uri']
          genres = ",".join(artist.get("genres"))
          followers = artist.get("Followers",{}).get("total",0)
          print(f"\n🎤 Name: {name}")
          print(f"🔥 Popularity: {popularity}")
          print(f"🎵 Genres: {genres}")
          print(f"👥 Followers: {followers}")
          print(f"🔗 URI: {uri}")
      else:
        print("No artist found.")
    else:
      print(f"Error: {response.status_code}{response.text}")
