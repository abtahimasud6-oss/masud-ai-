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
        # সরাসরি এবং ফাস্ট রেসপন্সের জন্য gemini-2.5-flash মডেল ব্যবহার
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
