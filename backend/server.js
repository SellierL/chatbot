const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

// Servir les fichiers statiques du frontend
const frontendPath = path.join(__dirname, 'frontend');
app.use(express.static(frontendPath));

const conversationsFilePath = path.join(__dirname, 'conversations.json');

// Charger les conversations depuis le fichier JSON
function loadConversations() {
  try {
    if (fs.existsSync(conversationsFilePath)) {
      const data = fs.readFileSync(conversationsFilePath, 'utf-8');
      return JSON.parse(data);
    }
    return [];
  } catch (err) {
    console.error("Erreur lors du chargement des conversations :", err);
    return [];
  }
}

// Sauvegarder les conversations dans le fichier JSON
function saveConversations(conversations) {
  try {
    fs.writeFileSync(conversationsFilePath, JSON.stringify(conversations, null, 2), 'utf-8');
    console.log("Conversations sauvegardées avec succès.");
  } catch (err) {
    console.error("Erreur lors de la sauvegarde des conversations :", err);
  }
}

// Endpoint pour charger les conversations
app.get('/api/loadConversations', (req, res) => {
  console.log("Requête reçue : /api/loadConversations");
  const conversations = loadConversations();
  res.json(conversations);
});

// Endpoint pour sauvegarder les conversations
app.post('/api/saveConversations', (req, res) => {
  console.log("Requête reçue : /api/saveConversations");
  const conversations = req.body;
  saveConversations(conversations);
  res.status(200).send('Conversations sauvegardées');
});

// Endpoint pour ajouter un nouveau message
app.post('/api/addMessage', (req, res) => {
  console.log("Requête reçue : /api/addMessage");
  const { userMessage, botResponse } = req.body;
  const conversations = loadConversations();

  if (conversations.length === 0) {
    conversations.push({ title: "Nouvelle conversation", messages: [] });
  }

  conversations[0].messages.push({ user: userMessage, bot: botResponse });
  saveConversations(conversations);

  res.status(200).send('Message ajouté et conversations mises à jour');
});

// Gérer les routes non trouvées
app.use((req, res) => {
  console.error(`Route non trouvée : ${req.method} ${req.url}`);
  res.status(404).send('Ressource non trouvée');
});

// Démarrer le serveur
app.listen(5000, () => {
  console.log('Serveur démarré sur le port 5000');
  console.log(`Frontend disponible sur http://127.0.0.1:5000`);
});