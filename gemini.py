import google.generativeai as genai

API_KEY = "api_key"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash-exp")
chat = model.start_chat()

print("chat with gemini")
while True:
    user_input = input("you: ")
    if user_input.lower() == "exit":
        break
    try:
        response = chat.send_message(user_input)
        print("gemini:", response.text)
    except Exception as e:
        print("Error:", e)