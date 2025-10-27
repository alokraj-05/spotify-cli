import subprocess
import os

def findNdLaunch(appName):
  commanPaths = [
    os.path.expandvars(rf'%APPDATA%\Spotify\Spotify.exe'),
    os.path.expandvars(rf'%LOCALAPPDATA%\{appName}\{appName}.exe'),
  ]

  for path in commanPaths:
    if os.path.exists(path):
      print(f"Found: {path}")
      subprocess.Popen([path])
      return True
  print(f"{appName} not found")
  return False