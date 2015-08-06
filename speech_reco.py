import speech_recognition as sr
import pyttsx as tts


class SpeechRecognition:
    def __init__(self, language="en-US", name=""):
        self.engine = tts.init()
        self.language = language
        self.recognizer = sr.Recognizer(language)
        self.recognizer.pause_threshold = 0.5
        self.recognizer.energy_threshold = 2500
        self.name = name
        self.err = "Commande non reconnue"

    def recognize(self):
        self.engine.say('Yes Sir ?')
        self.engine.runAndWait()
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source, timeout=3)
        try:
            work = self.recognizer.recognize(audio)
            return work
        except LookupError:
            return self.err


class Think:
    def __init__(self):
        self.engine = tts.init()
        self.default_answer = "Hi Sir"

    def execute(self, texte):
        #self.engine.say(self.default_answer)
        self.engine.runAndWait()
        return texte