from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"  # à adapter selon le modèle installé

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("message")
    
    payload = {
        "model": MODEL_NAME,
        "prompt": user_input,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    reply = response.json().get("response", "Erreur de réponse.")
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
