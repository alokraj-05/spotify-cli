from filter import voiceRec as vR
from Scripts.Playback import Playback
from Scripts.Artist import Artist
from login import login
from dotenv import load_dotenv
from filter import runApp as rA
import time
load_dotenv()
access_token = login();

playback = Playback(access_token)
artist = Artist(access_token)
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
    elif res.status_code == 200:
      playback.play(req)
      return
    else:
      return
  elif method == "pause":
    res = playback.pause()
    return
  elif method == "artist":
    res = artist.artist_name(req)
  else:
    return
  
def isReady(req):
    # Handle None/empty input
    if not req:
        print("❌ Could not understand audio input")
        return
    
    # Convert to string and normalize
    activation_word = str(req[0]).lower() if isinstance(req, list) else str(req).lower()
    
    # Check for exit command
    if activation_word == "exit":
        print("👋 Exiting voice control...")
        return
    
    # Check for activation word
    if activation_word == "hello":
        print("🎧 Listening for command...")
        command = vR.audioRec()
        
        # Handle failed command recognition
        if not command:
            print("❌ Could not understand command")
            # Continue listening
            next_input = vR.audioRec()
            return isReady(next_input)
            
        # Execute the command
        try:
            methodToDo(command[0], command[1])
        except Exception as e:
            print(f"❌ Error executing command: {e}")
        
        # Continue listening
        print("🎤 Say 'Meow' for new command or 'exit' to quit...")
        next_input = vR.audioRec()
        return isReady(next_input)
    
    # Not activated, keep listening
    print("🎤 Say 'Meow' to activate or 'exit' to quit...")
    next_input = vR.audioRec()
    return isReady(next_input)

# Update main execution
print("🎤 Say 'Meow' to activate or 'exit' to quit...")
initial_input = vR.audioRec()
print(initial_input)
isReady(initial_input)

