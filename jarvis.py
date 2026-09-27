import speech_recognition as sr
import pyttsx3
import time
import os
import sys

class Jarvis:
    def __init__(self):
        self.engine = pyttsx3.init()
        # i can adjust the voice and speed of the voice of jarvis
        # self.engine.setProperty('rate', 170)        
        self.recognizer = sr.Recognizer()
        self.is_active = False

    def speak(self, text):
        """Speak out the text and print it."""
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("\n[Listening...]")
            # Adjust for ambient noise briefly thats why i have given the 0.5 sec of delay
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return ""
        
        try:
            print("[Transcribing...]")
            # Using Google's free speech recognition
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"[Error: Could not request results from service; {e}]")
            return ""

    def process_command(self, text):
        # Wake word detection for jarvis
        if "jarvis" in text and not self.is_active:
            self.is_active = True
            self.speak("Yes, sir? I am listening.")
            return

        if not self.is_active:
            return

        # Stop listening command for jarvis
        if "stop listening" in text or "sleep" in text or "go to sleep" in text:
            self.speak("Going offline. Goodbye, sir.")
            self.is_active = False
            sys.exit(0)

        # simple commands 
        if "hello" in text or "hi" in text:
            self.speak("Hello! How can I assist you today?")
        elif "how are you" in text:
            self.speak("I am functioning at optimal capacity, sir.")
        elif "time" in text:
            current_time = time.strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}.")
        elif "date" in text:
            current_date = time.strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}.")
        else:
            self.speak("I heard you, but I don't know how to respond to that yet. LLM integration is pending.")

    def run(self):
        self.speak("JARVIS Version 1 initialized. Waiting for wake word 'Jarvis'.")
        print("\n(Tip: Say 'Jarvis' to wake up, then give commands like 'What is the time?' or 'Stop listening')")
        
        while True:
            try:
                text = self.listen()
                if text:
                    with open("jarvis_chat_log.txt", "a") as f:
                        f.write(f"You: {text}\n")

                    self.process_command(text)
            except KeyboardInterrupt:
                print("\n[Exiting JARVIS]")
                break
            except Exception as e:
                print(f"[An error occurred: {e}]")

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()
