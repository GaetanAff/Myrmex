# 🧠 TODO - Architecture d'un Backend Cognitif Distribué

## 1. Création d’un backend minimal
- Mettre en place un premier script local (CLI ou API simple).
- Ce backend reçoit une requête utilisateur et la transmet à **Ollama** installé localement pour traitement.

## 2. Analyse et planification
- Utiliser un prompt structuré pour analyser la requête et la découper en sous-tâches.
- Les sous-tâches sont catégorisées selon les types de traitement :
  - Raisonnement complexe (`deep_think_1`, `deep_think_2`, etc.)
  - Recherche d’informations (`deep_research_1`, `deep_research_2`, etc.)
- Chaque tâche est stockée comme un objet/variable distinct.

### Agents impliqués :
- **Agent planificateur (Top-Level Planning Agent)** : comprend la tâche globale, la découpe en sous-tâches, et coordonne les agents spécialisés.

## 3. Exécution distribuée des tâches
- Pour chaque tâche, lancement dynamique d’un script dédié :
  - `deep_think_agent`, `deep_research_agent`, etc.
- Chaque agent agit de façon autonome selon les instructions du planificateur.

### Agents spécialisés :
- **Deep Analyzer** : analyse de données textuelles ou structurées, extraction d’insights.
- **Deep Researcher** : recherche automatique, synthèse multi-source.
- **Browser Use Agent** : navigation web automatisée pour récupérer des données en ligne.
- **General Tool Calling Agent** : interface universelle pour interagir avec des APIs/outils externes.

## 4. Boucle adaptative avec garde-fou
- Les agents peuvent itérer leur raisonnement ou recherche si nécessaire.
- Un **script de validation (garde-fou)** surveille la conformité de chaque agent avec les instructions initiales.

## 5. Agrégation des résultats
- Une fois les tâches accomplies, un **script d’agrégation** combine les résultats.
- Génère une synthèse ou une réponse cohérente.

## 6. Vérification finale (fact-checking)
- Prend la question initiale et la réponse générée.
- Vérifie :
  - Pertinence de la réponse
  - Adéquation avec la requête initiale
  - Cohérence et validité factuelle (dans la mesure du possible via LLM)

## 7. Production de la réponse finale
- Si tout est validé par les étapes précédentes :
  - Génération de la **réponse finale** à renvoyer à l’utilisateur.

---

📌 **Remarque** : Chaque module doit rester découplé, facilement testable et extensible pour de futurs agents ou outils d'analyse.
