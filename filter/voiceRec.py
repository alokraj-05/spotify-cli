import speech_recognition as sr
import socket

def isOnline():
  try:
    socket.create_connection(("www.google.com",80))
    return True
  except:
    return False

def audioRec():
    if isOnline():
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            print("🎤 Listening...")
            audio = r.listen(source,timeout=5,phrase_time_limit=5)
            try:
                inp = r.recognize_google(audio)
                print(f"🗣️ Heard: {inp}")
                lst_out = inp.split(" ", 1)
                return lst_out if len(lst_out) > 0 else None
            except sr.UnknownValueError:
                print("🪛 Noisy background unknown input.")
                return None
            except sr.RequestError:
                print("❌ Could not request results from speech recognition service")
                return None
    else:
        print("❌ No Internet connection found.")
        return None




