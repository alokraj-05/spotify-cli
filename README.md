# Spotify CLI

<img width="1274" height="695" alt="Spotify-cli" src="https://github.com/user-attachments/assets/a88b9e02-59e0-4344-9ae8-d4b1e6bc7dad" />
> A tool to control your Spotify client via CLI commands, via calling function and providing parameters.

**What's the purpose?**

- GUI are for non other than normal user, I prefer CLI over GUI. So for that sake I created this tool and for those linux user who want to uses windows sometimes and want to use spotify via CLI.
- Clean your hands on api's methods and reponse types
- Used python to keep it simple for new programmers and students
- Simple understanding of moduler project (used oop concept for scalability)

**How to use**

1. Download the [package](https://github.com/alokraj-05/spotify-cli/packages) or [clone](https://github.com/alokraj-05/spotify-cli.git) the repository

```shell
git clone https://github.com/alokraj-05/spotify-cli.git
```

- If you downloaded the package
  - open the directory where the tool is located
  - In file address run cmd
  - Inside `CLI`
  ```shell
  spotifyCli login
  spotifyCli --help
  ```
  - And You are good to go
- If Clone the repository
  - In Terminal run
  ```shell
  pip install -r requirements.txt
  ```

  ```shell
  py main.py login
  py main.py --help
  ```
  > Note: There is a lot of things to do, the current version i.e 1.1 can run via commands and voice actions which supports [play,pause,exit]: in voice and [play,pause,seek,next,merge-playlist,create-playlist,add-multiple-songs]: in command.
  > Feel free to contribute 
