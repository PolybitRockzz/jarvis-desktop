from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import os
from win10toast import ToastNotifier

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
                return text
        except sr.UnknownValueError:
            speak(f"An error occured while listening, please repeat {user}")
            recog = sr.Recognizer()

# mappings functions

def greet():
    speak(f"Hello {user}, I am your personal assistant. How may I help you?")
    serve()

def open_app():
    speak("Opening app")

def nothing():
    speak("Ohh sorry")

def bye():
    speak(f"Goodbye {user}!")
    exit()

mappings = {
    'greet': greet,
    'open app': open_app,
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