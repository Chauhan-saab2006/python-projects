import webbrowser
import pyautogui
import pyperclip
import time

def send_whatsapp_message(contact: str, message: str):
    """Send a WhatsApp message to a contact using WhatsApp Web."""
    webbrowser.open("https://web.whatsapp.com/")
    time.sleep(10)  # Wait for WhatsApp Web to load
    pyperclip.copy(message)
    pyautogui.click(x=239, y=313)  # Adjust coordinates for the search bar
    time.sleep(3)
    pyautogui.write(contact)
    time.sleep(5)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.click(x=1086, y=965)  # Adjust coordinates for the message box
    pyautogui.hotkey("ctrl", "v")
    time.sleep(2)
    pyautogui.press("enter")
