import pyttsx3
import threading
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

# ⚠️ APNI GROQ KEY YAHAN DH dhyan se paste karein
# Check karein ki "gsk_..." se shuru ho rahi ho
try:
    client = Groq(api_key="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")
except:
    client = None

def speak(text):
    def run_voice():
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except: pass
    threading.Thread(target=run_voice, daemon=True).start()

def ask_ai(prompt):
    if not client:
        return "System is ready. How can I help you today?"
        
    try:
        # Purana model 'llama3-8b-8192' hata kar ye naya wala daalein:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant", # Ye super fast aur active model hai
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("Error:", e)
        return "I am MS AI. I am online and ready!"

@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("message", "")
    ai_reply = ask_ai(user_query)
    speak(ai_reply)
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)