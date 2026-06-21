from textual.app import App, ComposeResult
from textual.widgets import (
    Header, Footer, Static, Input,
    ProgressBar, ListView, ListItem, Label
)
from textual.containers import Horizontal, Vertical
from rich.text import Text
from rich.traceback import install
install(show_locals=True)

from login import login
from Scripts.Playback import Playback
from Scripts.Playlist import Playlist

session = login()

playback = Playback(session["access_token"])
playlist = Playlist(session["access_token"], session["sp"])


class SpotifyCLI(App):

    CSS = """
    Screen {
        background: black;
    }

    #sidebar {
        width: 28%;
        border: solid white;
    }

    #main {
        width: 72%;
        border: solid white;
    }

    #now_playing {
        height: 3;
        border: solid white;
    }

    #logo {
        content-align: center middle;
        height: 1fr;
    }

    #progress {
        height: 3;
    }

    #user_info {
        height: 5;
        border-top: solid white;
    }

    Input {
        border-top: solid white;
    }
    """

    # STEP 2
    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():

            with Vertical(id="sidebar"):
                yield Static("USER PLAYLISTS")

                yield ListView(
    *[
        ListItem(Label(pl["name"]))
        for pl in playlist.get_all_playlists()
    ]
)

                yield Static("USER INFO", id="user_info")

            with Vertical(id="main"):
                yield Static(
                    "Currently playing...",
                    id="now_playing"
                )

                yield Static(
                    Text("""░█▀▀░█▀█░█▀█░▀█▀░▀█▀░█▀▀░█░█░░░█▀▀░█░░░▀█▀
░▀▀█░█▀▀░█░█░░█░░░█░░█▀▀░░█░░░░█░░░█░░░░█░
░▀▀▀░▀░░░▀▀▀░░▀░░▀▀▀░▀░░░░▀░░░░▀▀▀░▀▀▀░▀▀▀
""", justify="center"),
                    id="logo"
                )

                yield ProgressBar(
                    total=100,
                    id="progress"
                )

                yield Input(
                    placeholder="Enter command..."
                )

        yield Footer()

    # STEP 3
    # Runs once when app starts
    def on_mount(self):
        self.set_interval(1, self.update_player)

    # STEP 4
    # Updates song info every second
    def update_player(self):
        current = playback.get_current_playing()

        now_playing = self.query_one("#now_playing", Static)
        progress = self.query_one("#progress", ProgressBar)

        if current:
            now_playing.update(
                f"{current['track']} - {current['artist']}"
            )

            progress.update(
                progress=current["progress"],
                total=current["duration"]
            )

        else:
            now_playing.update("Nothing playing")
            progress.update(progress=0)

    # STEP 6
    # Handles commands typed in input box
    async def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value.strip()

        if cmd.startswith("play "):
            playback.play(cmd[5:])

        elif cmd == "pause":
            playback.pause()

        elif cmd == "playlists":
            print(playlist.get_all_playlists())

        elif cmd == "exit":
            self.exit()

        event.input.value = ""


if __name__ == "__main__":
    try:
        SpotifyCLI().run()
    except Exception as e:
        print(e)
        input("Press Enter to exit...")