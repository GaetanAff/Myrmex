from flask import Flask, render_template, request, jsonify
import requests
import json
import re

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:12b"

@app.route('/')
def index():
    return render_template('index.html')

def extract_tasks_from_response(text: str):
    """Extrait et structure les tâches depuis la réponse d'Ollama."""
    try:
        # Cherche un JSON dans la réponse
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            if "tasks" in data:
                return data["tasks"]
    except Exception:
        pass
    
    # Si pas de JSON, essaie d'extraire manuellement
    tasks = []
    lines = text.split('\n')
    
    deep_think_count = 1
    deep_research_count = 1
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Détecte les indicateurs de tâches de réflexion
        if any(keyword in line.lower() for keyword in ['analyser', 'réfléchir', 'comprendre', 'évaluer', 'examiner', 'considérer']):
            task = {
                "id": f"deep_think_{deep_think_count}",
                "type": "deep_think",
                "description": line.replace('-', '').replace('*', '').strip()
            }
            tasks.append(task)
            deep_think_count += 1
            
        # Détecte les indicateurs de tâches de recherche
        elif any(keyword in line.lower() for keyword in ['rechercher', 'trouver', 'vérifier', 'consulter', 'chercher', 'données', 'information']):
            task = {
                "id": f"deep_research_{deep_research_count}",
                "type": "deep_research", 
                "description": line.replace('-', '').replace('*', '').strip()
            }
            tasks.append(task)
            deep_research_count += 1
    
    return tasks

def create_task_variables(tasks):
    """Crée des variables distinctes pour chaque tâche."""
    task_variables = {}
    
    for task in tasks:
        var_name = task["id"]
        task_variables[var_name] = {
            "id": task["id"],
            "type": task["type"],
            "description": task["description"],
            "status": "pending"
        }
    
    return task_variables

@app.route('/plan', methods=['POST'])
def plan_tasks():
    user_input = request.json.get("message", "")
    
    # Prompt optimisé pour le découpage de tâches
    planning_prompt = f"""
Tu es un expert en découpage de tâches. Analyse cette requête et découpe-la en sous-tâches spécifiques.

RÈGLES:
- Identifie les tâches de RÉFLEXION (analyse, évaluation, raisonnement)
- Identifie les tâches de RECHERCHE (collecte d'informations, vérification de données)
- Sois précis et détaillé dans chaque description
- Retourne un JSON avec cette structure exacte:

{{
  "tasks": [
    {{"id": "deep_think_1", "type": "deep_think", "description": "description détaillée"}},
    {{"id": "deep_research_1", "type": "deep_research", "description": "description détaillée"}}
  ]
}}

REQUÊTE À ANALYSER: {user_input}

Réponse:"""

    planning_payload = {
        "model": MODEL_NAME,
        "prompt": planning_prompt,
        "stream": False
    }
    
    tasks = []
    task_variables = {}
    raw_response = ""
    
    try:
        plan_response = requests.post(OLLAMA_API_URL, json=planning_payload)
        if plan_response.ok:
            raw_response = plan_response.json().get("response", "")
            tasks = extract_tasks_from_response(raw_response)
            task_variables = create_task_variables(tasks)
            
    except requests.RequestException as e:
        return jsonify({
            "error": f"Erreur de connexion: {str(e)}",
            "tasks": [],
            "task_variables": {},
            "raw_response": ""
        })
    
    return jsonify({
        "tasks": tasks,
        "task_variables": task_variables,
        "raw_response": raw_response,
        "total_tasks": len(tasks),
        "deep_think_count": len([t for t in tasks if t["type"] == "deep_think"]),
        "deep_research_count": len([t for t in tasks if t["type"] == "deep_research"])
    })

if __name__ == '__main__':
    app.run(debug=True)
