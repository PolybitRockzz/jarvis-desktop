from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import os
from win10toast import ToastNotifier
from pathlib import Path

recog = sr.Recognizer()

tts = pyttsx3.init()
tts.setProperty('voice', 'english+f1')
tts.setProperty('rate', 200)

user = os.getlogin()

def speak(text):
    tts.say(text)
    tts.runAndWait()

logon = AudioSegment.from_wav("audio\\logon.wav")
logoff = AudioSegment.from_wav("audio\\logoff.wav")

def quiet_listen():
    global recog
    while True:
        try:
            with sr.Microphone() as mic:
                audio = recog.listen(mic, timeout=10)
                text = recog.recognize_google(audio)
                print("> " + text)
                if text.lower() == "jarvis":
                    return True
                elif "jarvis" in text.lower():
                    return False
        except sr.UnknownValueError:
            recog = sr.Recognizer()
        except sr.WaitTimeoutError:
            print("...")

def listen():
    global recog
    while True:
        try:
            with sr.Microphone() as mic:
                play(logon)
                audio = recog.listen(mic)
                play(logoff)
                text = recog.recognize_google(audio)
                print("Query >> " + text)
                return text.lower()
        except sr.UnknownValueError:
            speak(f"An error occured while listening, please repeat {user}")
            recog = sr.Recognizer()

# mappings functions

def greet():
    speak(f"Hello {user}, I am your personal assistant, JARVIS. How may I help you?")
    serve()

def open_app():
    folder = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs'
    subfolderPaths = [ f.path for f in os.scandir(folder) if f.is_dir() ]
    subfolderNames = [ f.name for f in os.scandir(folder) if f.is_dir() ]
    shortcutPaths = [ f.path for f in os.scandir(folder) if f.is_file() ]
    shortcutNames = [ f.name[:-4] for f in os.scandir(folder) if f.is_file() ]

    for i in range(len(subfolderPaths)):
        paths = [ f.path for f in os.scandir(folder + '\\' + subfolderNames[i-1]) if f.is_file() ]
        names = [ f.name[:-4] for f in os.scandir(folder + '\\' + subfolderNames[i-1]) if f.is_file() ]
        shortcutPaths = shortcutPaths + paths
        shortcutNames = shortcutNames + names
    
    desktop = str(Path.home()) + '\\Desktop'

    desktopPaths = [ f.path for f in os.scandir(desktop) if f.is_file() ]
    desktopNames = [ f.name[:-4] for f in os.scandir(desktop) if f.is_file() ]
    shortcutPaths = shortcutPaths + desktopPaths
    shortcutNames = shortcutNames + desktopNames

    speak("Which application would you like to open?")
    available = [f for f in shortcutNames]
    while True:
        query = listen()
        if "quit" in query:
            speak("Okay")
            break
        temp = []
        search_terms = query.split(" ")
        for term in search_terms:
            for filename in available:
                if term in filename.lower():
                    temp = temp + [filename]
            available = temp
            temp = []
        if len(available) == 1:
            speak(f"Opening {available[0]}")
            os.startfile(shortcutPaths[shortcutNames.index(available[0])])
            break
        elif len(available) == 0:
            speak(f"I could not find {query}, please try again")
            speak(f"If {query} is installed in this machine, try adding it to the desktop or start menu")
            available = [f for f in shortcutNames]
        elif len(available) > 1:
            speak(f"There are {len(available)} applications available")
            for name in available:
                speak(name)
            speak("Could you be more specific about which one you would like to open?")

def time():
    import datetime
    hr12 = datetime.datetime.now().strftime("%I:%M %p")
    hr24 = datetime.datetime.now().strftime("%H:%M")
    speak("The time now is " + hr24 + "hours, or " + hr12)

def nothing():
    speak("Ohh sorry")

def bye():
    speak(f"Goodbye {user}!")
    exit()

mappings = {
    'greet': greet,
    'open app': open_app,
    'time': time,
    'nothing': nothing,
    'exit':bye
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()
# assistant.save_model()

def serve():
    query = listen()
    query = query.lower()
    assistant.request(query)

if __name__ == '__main__':
    start = ToastNotifier()
    start.show_toast("JARVIS is now online 👍", "JARVIS Desktop Assistant is now successfully running in the background.", duration=10, threaded=True)
    speak("JARVIS is now online!")
    while True:
        query = quiet_listen()
        if not query:
            speak("Did you need my help?")
            while True:
                ask1 = listen()
                if "yes" in ask1:
                    speak("Alright sir, how may I help?")
                    serve()
                    break
                elif "no" in ask1:
                    speak("My bad")
                    break
                else:
                    speak("I didn't get it, where you calling me?")
        elif query:
            speak("How may I help?")
            serve()
        else:
            pass