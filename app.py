from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# তোমার আসল API Key এখানে বসাবে
API_KEY = "YOUR_GEMINI_API_KEY"

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"Client Initialization Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"reply": "কোনো মেসেজ পাওয়া যায়নি।"})
        
    try:
        # এখানে system_instruction দিয়ে চ্যাটবটকে তোমার নাম শিখিয়ে দেওয়া হয়েছে
        config = types.GenerateContentConfig(
            system_instruction="তোমার নাম Masud AI। তোমাকে তৈরি করেছে Abtahi Masud YAFI (আবতাহী মাসূদ ইয়াফি)। কেউ যদি জিজ্ঞেস করে তোমাকে কে বানিয়েছে, তুমি গর্বের সাথে বলবে যে তোমাকে আবতাহী বানিয়েছে।"
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=config
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        error_msg = f"Error details: {str(e)}"
        print(error_msg)
        return jsonify({"reply": f"দুঃখিত, সমস্যা হয়েছে। {error_msg}"})

if __name__ == "__main__":
    # অটোমেটিক ngrok লাইভ লিংক তৈরি করার জন্য
    from pyngrok import ngrok
    try:
        public_url = ngrok.connect(5000)
        print("\n" + "="*50)
        print(f"👉 তোমার AI চ্যাটবটের অনলাইন লাইভ লিংক: {public_url}")
        print("="*50 + "\n")
    except Exception as e:
        print(f"Ngrok জেনারেট করতে সমস্যা হয়েছে: {e}")
        
    app.run(debug=True, use_reloader=False) # reloader বন্ধ করা হয়েছে যেন ngrok ডাবল কানেক্ট না হয়