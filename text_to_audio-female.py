from gtts import gTTS  # Import gTTS library
import os

# Get text input from the user
text = input("Enter the text you want to convert to audio: ")

# Convert text to speech
tts = gTTS(text=text, lang='en')  # 'en' for English

# Save the audio file
tts.save("output.mp3")

print("Audio file has been saved as output.mp3")

# Optional: Play the audio file (works on Windows)
os.system("start output.mp3")
