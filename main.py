import typer
from login import login
from dotenv import load_dotenv
from Scripts.Artist import Artist
from Scripts.Playback import Playback
from Scripts.Playlist import Playlist
from rich import print

load_dotenv()

app = typer.Typer(
    help="Spotify CLI - Control playback, playlists, and aritist"
)

session = login()
artist = Artist(session['access_token'])
playback = Playback(session['access_token'])
playlist = Playlist(session['access_token'],session['sp'])


@app.command()
def authenticate():
    login()

@app.command()
def play(song_name):
    playback.play(song_name)

@app.command()
def pause():
    playback.pause()

@app.command()
def artist_info(artist_name):
    artist.artist_name(artist_name)

@app.command()
def add(*data: str):
    playlist.add_songs(list(data))

@app.command()
def play_playlist(link:str):
    playback.play_playlist(link)

@app.command()
def merge_playlist_command(playlist_name:str,playlist1_url:str,playlist2_url:str):
    playback.merge_playlist(playlist_name,playlist1_url,playlist2_url)

@app.command()
def get_playlists(name:str):
    playlist.get_playlist_id(name)


if __name__ == "__main__":
    app()
