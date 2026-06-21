from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.panel import Panel
import shlex
from main import app

console = Console()

COMMANDS = [
    "play",
    "pause",
    "artist-info",
    "playlists",
    "add",
    "merge",
    "playlist"
    "help",
    "exit"
]

completer = WordCompleter(COMMANDS, ignore_case=True)

session = PromptSession(
    history=FileHistory(".spotify_history")
)


def banner():
    console.print(
        Panel.fit(
            """[bold green]░█▀▀░█▀█░█▀█░▀█▀░▀█▀░█▀▀░█░█░░░█▀▀░█░░░▀█▀
░▀▀█░█▀▀░█░█░░█░░░█░░█▀▀░░█░░░░█░░░█░░░░█░
░▀▀▀░▀░░░▀▀▀░░▀░░▀▀▀░▀░░░░▀░░░░▀▀▀░▀▀▀░▀▀▀""",
            title="Welcome"
        )
    )


def run_shell():
    banner()

    while True:
        try:
            text = session.prompt(
                "spotify> ",
                completer=completer
            ).strip()

            if not text:
                continue

            if text.lower() in ["exit", "quit"]:
                console.print("[red]Goodbye[/red]")
                break

            if text.lower() == "help":
                app(["--help"])
                continue

            args = shlex.split(text)

            try:
                app(args, standalone_mode=False)
            except Exception as e:
                console.print(f"[red]{e}[/red]")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    run_shell()