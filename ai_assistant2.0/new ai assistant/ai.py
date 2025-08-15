import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import subprocess
import os
import pygetwindow
import win32gui
import win32con

# Text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen for voice commands
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
    except:
        command = ""
    return command.lower()

# Helper: format website name to URL
def get_website_url(command):
    site_name = command.replace("open", "").strip()
    if not site_name:
        return None
    if "." not in site_name:
        site_name += ".com"
    url = f"https://{site_name}"
    return url

# Software paths
software_paths = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "visual studio code": r"C:\Users\YourUsername\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
}

# Open software
def open_software(command):
    for name, path in software_paths.items():
        if name in command:
            try:
                subprocess.Popen(path)
                speak(f"Opening {name}")
                return True
            except Exception as e:
                speak(f"Could not open {name}. Error: {e}")
                return True
    return False

# Close software
def close_software(command):
    for name, path in software_paths.items():
        if name in command:
            process_name = os.path.basename(path)
            try:
                os.system(f"taskkill /f /im {process_name}")
                speak(f"Closing {name}")
                return True
            except Exception as e:
                speak(f"Could not close {name}. Error: {e}")
                return True

    if "browser" in command or "chrome" in command:
        os.system("taskkill /f /im chrome.exe")
        speak("Closing Chrome browser")
        return True
    elif "firefox" in command:
        os.system("taskkill /f /im firefox.exe")
        speak("Closing Firefox browser")
        return True
    elif "edge" in command:
        os.system("taskkill /f /im msedge.exe")
        speak("Closing Microsoft Edge")
        return True

    return False

# Minimize software
def minimize_software(command):
    for window in pygetwindow.getAllTitles():
        for name in software_paths:
            if name in command and name.lower() in window.lower():
                try:
                    hwnd = win32gui.FindWindow(None, window)
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                    speak(f"Minimizing {name}")
                    return True
                except Exception as e:
                    speak(f"Could not minimize {name}. Error: {e}")
                    return True
    return False

# Maximize software
def maximize_software(command):
    for window in pygetwindow.getAllTitles():
        for name in software_paths:
            if name in command and name.lower() in window.lower():
                try:
                    hwnd = win32gui.FindWindow(None, window)
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    speak(f"Maximizing {name}")
                    return True
                except Exception as e:
                    speak(f"Could not maximize {name}. Error: {e}")
                    return True
    return False

# Create folder
def create_folder(command):
    if "create folder" in command:
        folder_name = command.replace("create folder", "").strip()
        if folder_name == "":
            speak("Please specify a folder name.")
            return True
        base_path = os.path.join(os.path.expanduser("~"), "Desktop")
        folder_path = os.path.join(base_path, folder_name)
        try:
            os.makedirs(folder_path, exist_ok=True)
            speak(f"Folder named {folder_name} created on Desktop.")
        except Exception as e:
            speak(f"Could not create folder. Error: {e}")
        return True
    return False

# Main assistant loop
def run_assistant():
    speak("Hello, how can I help you?")
    while True:
        command = take_command()

        if 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The time is {time}")

        elif command.startswith('open '):
            if open_software(command):
                continue
            url = get_website_url(command)
            if url:
                webbrowser.open(url)
                speak(f"Opening {url}")
            else:
                speak("Sorry, I couldn't understand the website.")

        elif command.startswith('close '):
            if close_software(command):
                continue
            else:
                speak("Sorry, I couldn't find the software or browser to close.")

        elif command.startswith('minimize ') or command.startswith('minimise '):
            if minimize_software(command):
                continue
            else:
                speak("Sorry, I couldn't minimize the window.")

        elif command.startswith('maximize '):
            if maximize_software(command):
                continue
            else:
                speak("Sorry, I couldn't maximize the window.")

        elif command.startswith('create folder'):
            if create_folder(command):
                continue

        elif 'search' in command:
            search_query = command.replace('search', '')
            url = f"https://www.google.com/search?q={search_query.strip()}"
            webbrowser.open(url)
            speak(f"Searching for {search_query}")

        elif 'exit' in command or 'quit' in command:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that.")

# Run the assistant
run_assistant()
