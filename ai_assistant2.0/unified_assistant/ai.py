import google.generativeai as genai

# Default Gemini model and API key (replace with your own if needed)
API_KEY = "AIzaSyDgyyTgp3_rpm2U2nqCIiNzuksCeADQouA"
MODEL_NAME = "gemini-2.0-flash-exp"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
chat = model.start_chat()

def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the response text."""
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"[Error from Gemini AI: {e}]"


