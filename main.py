from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"  # à adapter selon le modèle installé

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("message")

    plan_prompt = (
        "Tu es un agent de planification. Analyse la requête suivante et "
        "découpe-la en sous-tâches. Catégorise chaque sous-tâche par 'type' "
        "('deep_think' ou 'deep_research'). Retourne un JSON avec une liste "
        "'tasks' où chaque entrée est un objet {\"id\": \"deep_think_1\", "
        "\"type\": \"deep_think\", \"description\": \"...\"}. "
        f"Requête: {user_input}"
    )

    planning_payload = {
        "model": MODEL_NAME,
        "prompt": plan_prompt,
        "stream": False
    }
    plan_response = requests.post(OLLAMA_API_URL, json=planning_payload)
    tasks = []
    if plan_response.ok:
        try:
            tasks = json.loads(plan_response.json().get("response", "{}"))
            tasks = tasks.get("tasks", [])
        except json.JSONDecodeError:
            tasks = []

    payload = {
        "model": MODEL_NAME,
        "prompt": user_input,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    reply = response.json().get("response", "Erreur de réponse.")
    return jsonify({"reply": reply, "tasks": tasks})

if __name__ == '__main__':
    app.run(debug=True)
