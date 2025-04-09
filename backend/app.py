from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"
CONVERSATIONS_FILE = "conversations.json"

# Route principale pour servir index.html
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Endpoint API pour le chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "Message manquant"}), 400

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": user_message,
        "stream": False
    })

    if response.status_code == 200:
        ai_reply = response.json().get("response", "")
        return jsonify({"response": ai_reply})
    else:
        return jsonify({"error": "Erreur lors de la génération"}), 500

# Endpoint pour charger les conversations
@app.route("/api/loadConversations", methods=["GET"])
def load_conversations():
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as file:
            conversations = json.load(file)
        return jsonify(conversations)
    else:
        return jsonify([])  # Retourne une liste vide si le fichier n'existe pas

# Endpoint pour sauvegarder les conversations
@app.route("/api/saveConversations", methods=["POST"])
def save_conversations():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "Format de données invalide"}), 400

    try:
        with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return jsonify({"message": "Conversations sauvegardées avec succès"}), 200
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la sauvegarde : {str(e)}"}), 500

# Endpoint pour ajouter un nouveau message
@app.route("/api/addMessage", methods=["POST"])
def add_message():
    data = request.get_json()
    user_message = data.get("userMessage", "")
    bot_response = data.get("botResponse", "")

    if not user_message or not bot_response:
        return jsonify({"error": "Données manquantes"}), 400

    try:
        # Charger les conversations existantes
        if os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as file:
                conversations = json.load(file)
        else:
            conversations = []

        # Ajouter une nouvelle conversation si aucune n'existe
        if not conversations:
            conversations.append({"title": "Nouvelle conversation", "messages": []})

        # Ajouter le message utilisateur et la réponse du bot
        conversations[0]["messages"].append({"user": user_message, "bot": bot_response})

        # Sauvegarder les conversations mises à jour
        with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as file:
            json.dump(conversations, file, ensure_ascii=False, indent=2)

        return jsonify({"message": "Message ajouté avec succès"}), 200
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'ajout du message : {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)