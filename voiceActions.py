from filter import voiceRec as vR
from Scripts.Playback import Playback
from Scripts.Artist import Artist
from login import login
from dotenv import load_dotenv
from filter import runApp as rA
import time
import threading
import queue

load_dotenv()
access_token = login();
command_queue = queue.Queue()
bars = 50
playback = Playback(access_token)
artist = Artist(access_token)

def listener_thread():
   while True:
      try:
         req = vR.audioRec()
         if req:
            command_queue.put(req)
      except Exception as e:
         print('Listner error:',e)
         continue



def methodToDo(method,req):
  if method == "play":
    res = playback.play(req)
    if res.status_code  == 404:
      appLunched = rA.findNdLaunch("Spotify")
      if appLunched:
        time.sleep(3)
        playback.play(req)
        return
      else:
        return
    else:
      return
  elif method == "stop":
    res = playback.pause()
    return
  elif method == "artist":
    res = artist.artist_name(req)
    return
  else:
    print(f"Unhandled method: {method}")
    return
  
def isReady():
    print("🎤 Say 'Hello' for new command or 'exit' to quit...")
    active = False
    last_activity = time.time()
    TIMEOUT = 15

    while True:
        try:
          req = command_queue.get(timeout=0.5)
        except queue.Empty:
          if active and (time.time() - last_activity>TIMEOUT):
            print("💤 Going to sleep...")
            active = False
          continue
        print(req)
    
        text = str(req[0]).lower() if isinstance(req, list) else str(req).lower()
        if text == "exit":
            print("👋 Exiting voice control...")
            break
          
        if not active: 
          if text == "hello":
              print("🟢 Activated. Listening for command...")
              active = True
              last_activity = time.time()
          else:
              print("Sleeping... Say 'Hello' to wake me.")
          continue
        last_activity = time.time()
        if isinstance(req, list) and len(req) >= 2:
          methodToDo(req[0].lower(), req[1])
        else:
          print('❌ Invalid command format')
        


print("""
 _______  _____   _____  _______ _____ _______ __   __ _______        _____
 |______ |_____] |     |    |      |   |______   \_/   |       |        |  
 ______| |       |_____|    |    __|__ |          |    |_____  |_____ __|__
""")
t = threading.Thread(target=listener_thread, daemon=True)
t.start()
isReady()

