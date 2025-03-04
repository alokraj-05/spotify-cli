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
    artist.artist_name("kk")

@click.command()
@click.argument("song_name")
def play(song_name):
    playback.play(song_name)


main.add_command(authenticate)
main.add_command(artist_name)
main.add_command(play)


if __name__ == "__main__":
    main()  
