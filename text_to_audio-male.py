
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Set properties
voices = engine.getProperty('voices')
# voices[0] is usually male, voices[1] female (depends on OS)
engine.setProperty('voice', voices[0].id)  # Select male voice
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Get text input
text = input("Enter the text you want to convert to audio: ")

# Save to file
engine.save_to_file(text, 'output_male_voice.mp3')

# Speak out loud (optional)
engine.say(text)
engine.runAndWait()

print("Audio saved as output_male_voice.mp3")
