import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Render-এর Environment Variable থেকে Groq API Key নিবে
api_key = os.environ.get("GROQ_API_KEY")

try:
    client = Groq(api_key=api_key)
except Exception as e:
    client = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not client or not api_key:
        return jsonify({"error": "Groq API Key configuration missing অথবা ভুল।"}), 500
        
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        # Groq-এর সবচেয়ে ফাস্ট এবং ফ্রি মডেল llama-3.3-70b-versatile ব্যবহার করা হয়েছে
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        bot_reply = completion.choices[0].message.content
        return jsonify({"response": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
