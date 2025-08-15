import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import threading

from unified_assistant.voice import speak, listen
from unified_assistant.ai import ask_gemini
from unified_assistant.web import open_website, open_url, google_search
from unified_assistant.apps import open_software, close_software, minimize_software, maximize_software
from unified_assistant.media import play_music
from unified_assistant.messaging import send_whatsapp_message
from unified_assistant.files import create_folder, delete_folder, list_folders
from unified_assistant.news import get_top_headlines
from unified_assistant.utils import log

class UnifiedAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified AI Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#181818")

        # Chat area
        self.chat_box = scrolledtext.ScrolledText(root, font=("Segoe UI", 12), bg="#222", fg="#fff", state="disabled", wrap="word", height=20)
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))

        # User input
        self.input_frame = tk.Frame(root, bg="#181818")
        self.input_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        self.user_input = tk.Entry(self.input_frame, font=("Segoe UI", 12), bg="#333", fg="#fff")
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind('<Return>', self.send_message)
        self.send_btn = tk.Button(self.input_frame, text="Send", command=self.send_message, bg="#0e76a8", fg="#fff", font=("Segoe UI", 11, "bold"))
        self.send_btn.pack(side=tk.LEFT)
        self.voice_btn = tk.Button(self.input_frame, text="🎤", command=self.voice_input, bg="#444", fg="#fff", font=("Segoe UI", 11, "bold"))
        self.voice_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Feature buttons
        self.feature_frame = tk.Frame(root, bg="#181818")
        self.feature_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        tk.Button(self.feature_frame, text="Open Website", command=self.open_website_dialog, bg="#444", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(self.feature_frame, text="Google Search", command=self.google_search_dialog, bg="#444", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(self.feature_frame, text="Play Music", command=self.play_music_dialog, bg="#444", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(self.feature_frame, text="WhatsApp Msg", command=self.whatsapp_dialog, bg="#444", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(self.feature_frame, text="Create Folder", command=self.create_folder_dialog, bg="#444", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(self.feature_frame, text="Delete Folder", command=self.delete_folder_dialog, bg="#444", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(self.feature_frame, text="News", command=self.show_news, bg="#444", fg="#fff").pack(side=tk.LEFT, padx=5)

        # App control buttons
        self.app_frame = tk.Frame(root, bg="#181818")
        self.app_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        tk.Button(self.app_frame, text="Open App", command=self.open_app_dialog, bg="#333", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(self.app_frame, text="Close App", command=self.close_app_dialog, bg="#333", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(self.app_frame, text="Minimize App", command=self.minimize_app_dialog, bg="#333", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(self.app_frame, text="Maximize App", command=self.maximize_app_dialog, bg="#333", fg="#fff").pack(side=tk.LEFT, padx=5)

        self.user_input.focus_set()
        self.speak_and_insert("Hello! How can I help you today?")

    def speak_and_insert(self, text):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, f"AI: {text}\n")
        self.chat_box.see(tk.END)
        self.chat_box.config(state="disabled")
        threading.Thread(target=speak, args=(text,), daemon=True).start()

    def send_message(self, event=None):
        user_msg = self.user_input.get().strip()
        if not user_msg:
            return
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, f"You: {user_msg}\n")
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)
        self.user_input.delete(0, tk.END)
        threading.Thread(target=self.handle_ai_response, args=(user_msg,), daemon=True).start()

    def handle_ai_response(self, user_msg):
        response = ask_gemini(user_msg)
        self.speak_and_insert(response)

    def voice_input(self):
        self.speak_and_insert("Listening...")
        def listen_and_send():
            text = listen()
            if text:
                self.user_input.delete(0, tk.END)
                self.user_input.insert(0, text)
                self.send_message()
            else:
                self.speak_and_insert("Sorry, I didn't catch that.")
        threading.Thread(target=listen_and_send, daemon=True).start()

    def open_website_dialog(self):
        site = simpledialog.askstring("Open Website", "Enter website name (e.g., youtube, google):")
        if site:
            if open_website(site):
                self.speak_and_insert(f"Opening {site}.")
            else:
                self.speak_and_insert(f"Sorry, I don't know that website.")

    def google_search_dialog(self):
        query = simpledialog.askstring("Google Search", "Enter search query:")
        if query:
            google_search(query)
            self.speak_and_insert(f"Searching Google for '{query}'.")

    def play_music_dialog(self):
        song = simpledialog.askstring("Play Music", "Enter song name:")
        if song:
            play_music(song)
            self.speak_and_insert(f"Playing '{song}' on YouTube.")

    def whatsapp_dialog(self):
        contact = simpledialog.askstring("WhatsApp Message", "Enter contact name:")
        message = simpledialog.askstring("WhatsApp Message", "Enter message:")
        if contact and message:
            threading.Thread(target=send_whatsapp_message, args=(contact, message), daemon=True).start()
            self.speak_and_insert(f"Sending WhatsApp message to {contact}.")

    def create_folder_dialog(self):
        folder = simpledialog.askstring("Create Folder", "Enter folder name:")
        if folder:
            path = create_folder(folder)
            self.speak_and_insert(f"Folder '{folder}' created on Desktop.")

    def delete_folder_dialog(self):
        folder = simpledialog.askstring("Delete Folder", "Enter folder name:")
        if folder:
            if delete_folder(folder):
                self.speak_and_insert(f"Folder '{folder}' deleted from Desktop.")
            else:
                self.speak_and_insert(f"Folder '{folder}' not found.")

    def show_news(self):
        headlines = get_top_headlines()
        if headlines:
            for article in headlines:
                if 'error' in article:
                    self.speak_and_insert(article['error'])
                else:
                    self.speak_and_insert(f"{article['title']} (Source: {article['source']})")
        else:
            self.speak_and_insert("No news found.")

    def open_app_dialog(self):
        app = simpledialog.askstring("Open App", "Enter app name (e.g., notepad, chrome):")
        if app:
            if open_software(app):
                self.speak_and_insert(f"Opening {app}.")
            else:
                self.speak_and_insert(f"Could not open {app}.")

    def close_app_dialog(self):
        app = simpledialog.askstring("Close App", "Enter app name:")
        if app:
            if close_software(app):
                self.speak_and_insert(f"Closing {app}.")
            else:
                self.speak_and_insert(f"Could not close {app}.")

    def minimize_app_dialog(self):
        app = simpledialog.askstring("Minimize App", "Enter app name:")
        if app:
            if minimize_software(app):
                self.speak_and_insert(f"Minimizing {app}.")
            else:
                self.speak_and_insert(f"Could not minimize {app}.")

    def maximize_app_dialog(self):
        app = simpledialog.askstring("Maximize App", "Enter app name:")
        if app:
            if maximize_software(app):
                self.speak_and_insert(f"Maximizing {app}.")
            else:
                self.speak_and_insert(f"Could not maximize {app}.")

def launch_gui():
    root = tk.Tk()
    app = UnifiedAssistantGUI(root)
    root.mainloop()
