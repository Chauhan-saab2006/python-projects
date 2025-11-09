import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Set properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Select male voice
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Text input
text = "Kya aap aksar unit aur currency conversion mein time barbaad karte hain? To miliye Convertify se!"

# Save to file
engine.save_to_file(text, 'output_male_voice.mp3')

# Speak out loud (optional)
engine.say(text)
engine.runAndWait()

print("Audio saved as output_male_voice.mp3")
