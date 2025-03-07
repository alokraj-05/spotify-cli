import os
from login import login
from spotipy import Spotify
from dotenv import load_dotenv
import click
from Scripts.Artist import Artist
from Scripts.Playback import Playback
load_dotenv()
access_token = login()

artist = Artist(access_token)
playback = Playback(access_token)
    

@click.group()
def main():
    pass


@click.command()
def authenticate():
    login()

@click.command()
@click.argument("artist_name")
def artist_name(artist_name):
    artist.artist_name(artist_name)


@click.command()
@click.argument("song_name")
def play(song_name):
    playback.play(song_name)


@click.command()
@click.argument("link")
def play_playlist(link):
    playback.play_playlist(link)

@click.command()
def pause():
    playback.pause()


@click.command(name="merge-playlist")
@click.argument("playlist_name")
@click.argument("playlist1_url")
@click.argument("playlist2_url")
def merge_playlist_command(playlist_name,playlist1_url,playlist2_url):
    playback.merge_playlist(playlist_name,playlist1_url,playlist2_url)



main.add_command(authenticate)
main.add_command(artist_name)
main.add_command(play)
main.add_command(play_playlist)
main.add_command(pause)
main.add_command(merge_playlist_command)


if __name__ == "__main__":
    main()  
