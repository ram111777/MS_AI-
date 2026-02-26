import threading
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
# Sabhi origins allow karne ke liye (Frontend connectivity fix)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# API Key Environment Variable se uthayega (Security ke liye best hai)
api_key = os.environ.get("GROQ_API_KEY", "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")

try:
    client = Groq(api_key=api_key)
except Exception as e:
    print(f"Groq Client Error: {e}")
    client = None

# Render pe awaaz nahi nikal sakti, isliye isse sirf local ke liye rakha hai
def speak(text):
    # Server pe speaker nahi hota, isliye Render pe ye skip ho jayega
    if os.environ.get("RENDER"): 
        return
    
    # Local pe chalane ke liye pyttsx3 import yahan andar kiya hai
    try:
        import pyttsx3
        def run_voice():
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except: pass
        threading.Thread(target=run_voice, daemon=True).start()
    except ImportError:
        pass

def ask_ai(prompt):
    if not client:
        return "Groq Client not configured properly."
        
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("Groq API Error:", e)
        return "I am MS AI. I am online and ready!"

@app.route("/")
def home():
    # Check karein ki index.html sahi folder mein hai
    return "Backend is Running! Connect your frontend to /chat"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
        
    user_query = request.json.get("message", "")
    ai_reply = ask_ai(user_query)
    
    # Render pe awaaz nahi aayegi, sirf text return hoga
    speak(ai_reply) 
    
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    # RENDER PE YE DO LINES ZAROORI HAIN:
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
