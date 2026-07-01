import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Render-এর Environment Variable থেকে API Key নিবে
api_key = os.environ.get("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    client = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not client:
        return jsonify({"error": "API Key configuration missing অথবা ভুল।"}), 500
        
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        # gemini-2.5-flash মডেলের জন্য কন্টেন্ট জেনারেশন লজিক
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        
        # রেসপন্স টেক্সট চেক করা
        if response and response.text:
            bot_reply = response.text
        else:
            bot_reply = "দুঃখিত, আমি কোনো উত্তর তৈরি করতে পারিনি। দয়া করে আবার চেষ্টা করুন।"
            
        return jsonify({"response": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
