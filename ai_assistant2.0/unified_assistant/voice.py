import speech_recognition as sr
import pyttsx3

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def set_voice(gender: str = None):
    """
    Optionally set the voice to male/female if available.
    gender: 'male', 'female', or None for default.
    """
    voices = engine.getProperty('voices')
    if gender:
        for voice in voices:
            if gender.lower() in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

def speak(text: str):
    """Speak the given text using TTS."""
    engine.say(text)
    engine.runAndWait()

def listen(timeout: int = 5, phrase_time_limit: int = 8) -> str:
    """
    Listen for a command from the user using the microphone and return the recognized text.
    Returns None if not understood.
    """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"Some error occurred: {e}")
            return None
