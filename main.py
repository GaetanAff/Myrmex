from flask import Flask, render_template, request, jsonify
import requests
import json
import re

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"  # à adapter selon le modèle installé

@app.route('/')
def index():
    return render_template('index.html')

def extract_tasks(text: str):
    """Return a list of tasks extracted from an Ollama response."""
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return []
        data = json.loads(match.group())
        return data.get("tasks", [])
    except Exception:
        return []


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
    tasks = []
    try:
        plan_response = requests.post(OLLAMA_API_URL, json=planning_payload)
        if plan_response.ok:
            text = plan_response.json().get("response", "")
            tasks = extract_tasks(text)
    except requests.RequestException:
        pass

    payload = {
        "model": MODEL_NAME,
        "prompt": user_input,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        reply = response.json().get("response", "Erreur de réponse.")
    except requests.RequestException:
        reply = "Erreur: impossible de joindre le modèle."

    return jsonify({"reply": reply, "tasks": tasks})

if __name__ == '__main__':
    app.run(debug=True)
