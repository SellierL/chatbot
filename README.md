# Chatbot IA - llama3.2

Ce projet est un chatbot basé sur Flask pour le backend et une interface utilisateur moderne pour le frontend.

## Prérequis

- Python 3.8 ou supérieur
- `pip` (gestionnaire de paquets Python)
- `virtualenv` (optionnel mais recommandé)

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/SellierL/chatbot.git
   cd chatbot
   ```

2. Accédez au dossier `backend` :
   ```bash
   cd backend
   ```

3. Créez un environnement virtuel (optionnel mais recommandé) :
   ```bash
   python -m venv appEnv
   ```

4. Activez l'environnement virtuel :
   - Sur Windows :
     ```bash
     appEnv\Scripts\Activate
     ```
   - Sur macOS/Linux :
     ```bash
     source appEnv/bin/activate
     ```

5. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Lancer le projet

1. Assurez-vous d'être dans le dossier `backend` et que l'environnement virtuel est activé.

2. Lancez le serveur Flask :
   ```bash
   python app.py
   ```

3. Ouvrez votre navigateur et accédez à :
   ```
   http://127.0.0.1:5000
   ```

## Structure du projet

- `backend/` : Contient le backend Flask.
- `frontend/` : Contient les fichiers statiques pour l'interface utilisateur.
- `conversations.json` : Fichier JSON pour stocker les conversations.

---
