# 📋 Plan de Travail - Smart Bus IoT
## Communication Raspberry Pi → PC avec Dashboard

---

## 🎯 Vue d'ensemble

**Objectif** : Créer un système complet où la Raspberry Pi envoie les données des capteurs au PC, qui les stocke et les affiche dans un dashboard web.

---

## 📊 Options de Stack Technique

### Option 1 : Flask + SQLite (Simple)
- ✅ Facile à mettre en place
- ✅ Pas de dépendances externes
- ✅ Parfait pour prototype/développement

### Option 2 : FastAPI + SQLite (Moderne)
- ✅ API moderne et performante
- ✅ Documentation automatique (Swagger)
- ✅ Support async natif
- ✅ Meilleur pour production

### Option 3 : Flask/FastAPI + Firebase Firestore (Cloud)
- ✅ Base de données cloud (pas d'installation locale)
- ✅ Accès depuis n'importe où
- ✅ Scalable automatiquement
- ✅ Temps réel intégré

---

## 🔄 Étapes du Plan de Travail

### **ÉTAPE 1 : Préparer la Raspberry Pi**
- [ ] Vérifier que tous les capteurs fonctionnent (`main.py`)
- [ ] Installer `requests` pour les requêtes HTTP
  ```bash
  pip install requests
  ```
- [ ] Ajouter la configuration du serveur PC dans `config/config.json`
  ```json
  "server": {
    "enabled": true,
    "url": "http://192.168.1.100:5000",
    "timeout": 5,
    "retry_count": 3,
    "bus_id": "Bus1"
  }
  ```
- [ ] Créer un module `utils/http_client.py` pour envoyer les données
- [ ] Modifier `main.py` pour intégrer l'envoi HTTP POST après chaque collecte

**Livrable** : Raspberry Pi envoie des JSON au PC via HTTP POST

---

### **ÉTAPE 2 : Installer le Serveur API sur PC**

#### **Option A : Flask**
- [ ] Installer Flask sur le PC
  ```bash
  pip install flask flask-cors
  ```
- [ ] Créer `server/app.py` avec Flask
- [ ] Endpoints à créer :
  - `POST /api/data` - Recevoir les données de la Pi
  - `GET /api/latest` - Dernière donnée
  - `GET /api/health` - Vérifier que le serveur fonctionne

#### **Option B : FastAPI**
- [ ] Installer FastAPI sur le PC
  ```bash
  pip install fastapi uvicorn python-multipart
  ```
- [ ] Créer `server/main.py` avec FastAPI
- [ ] Mêmes endpoints que Flask
- [ ] Documentation auto sur `http://localhost:8000/docs`

#### **Option C : Firebase Firestore**
- [ ] Créer un projet Firebase
- [ ] Installer Firebase Admin SDK
  ```bash
  pip install firebase-admin
  ```
- [ ] Configurer les credentials Firebase
- [ ] Créer l'API qui écrit dans Firestore

**Livrable** : Serveur API fonctionnel sur PC (port 5000 ou 8000)

---

### **ÉTAPE 3 : Configuration Réseau (Raspberry → PC)**

- [ ] Trouver l'IP locale du PC
  - Windows : `ipconfig` → IPv4 Address
  - Linux/Mac : `ifconfig` ou `ip addr`
- [ ] Vérifier que Raspberry Pi et PC sont sur le même réseau
- [ ] Tester la connectivité depuis la Pi
  ```bash
  ping 192.168.1.100  # Remplacer par l'IP du PC
  ```
- [ ] Configurer le firewall du PC pour autoriser le port (5000 ou 8000)
  - Windows : Règle de pare-feu entrante
  - Linux : `sudo ufw allow 5000`
- [ ] Mettre à jour l'URL dans `config/config.json` de la Pi

**Livrable** : Communication réseau établie entre Pi et PC

---

### **ÉTAPE 4 : Dashboard HTML**

- [ ] Créer `server/dashboard/index.html`
- [ ] Intégrer Chart.js pour les graphiques
  ```html
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  ```
- [ ] Créer une fonction JavaScript qui appelle `/api/latest` toutes les 2-5 secondes
- [ ] Afficher :
  - Nombre de passagers (avec barre de progression)
  - GPS (latitude, longitude, vitesse)
  - Température et humidité
  - Accélération (X, Y, Z)
  - Graphiques en temps réel
- [ ] Ajouter un indicateur de statut (en ligne/hors ligne)

**Livrable** : Dashboard web fonctionnel accessible sur `http://localhost:5000` ou `http://localhost:8000`

---

### **ÉTAPE 5 : Base de Données (Optionnel mais Recommandé)**

#### **Option A : SQLite (Local)**
- [ ] Installer SQLite (déjà inclus avec Python)
- [ ] Créer une table dans le serveur Flask/FastAPI
  ```sql
  CREATE TABLE bus_data (
      id INTEGER PRIMARY KEY,
      timestamp TEXT,
      bus_id TEXT,
      data TEXT,
      created_at TEXT
  )
  ```
- [ ] Modifier `POST /api/data` pour sauvegarder dans SQLite
- [ ] Modifier `GET /api/latest` pour lire depuis SQLite

#### **Option B : Firebase Firestore**
- [ ] Créer une collection `bus_data` dans Firestore
- [ ] Écrire les données dans Firestore lors de `POST /api/data`
- [ ] Lire depuis Firestore pour `GET /api/latest`
- [ ] Avantage : Accès depuis n'importe où, pas besoin de serveur local

**Livrable** : Données stockées et récupérables depuis la base

---

### **ÉTAPE 6 : WebSocket pour Temps Réel (Optionnel)**

- [ ] Installer Flask-SocketIO ou FastAPI WebSocket
  ```bash
  # Flask
  pip install flask-socketio
  
  # FastAPI (déjà inclus)
  # Utiliser WebSocket natif
  ```
- [ ] Créer un endpoint WebSocket dans le serveur
- [ ] Modifier le dashboard pour utiliser WebSocket au lieu de polling
- [ ] Envoyer les nouvelles données automatiquement quand reçues

**Livrable** : Mise à jour en temps réel sans polling

---

## 🚀 Ordre d'Exécution Recommandé

1. **Étape 1** → Préparer la Raspberry Pi
2. **Étape 2** → Installer le serveur API sur PC (choisir Flask, FastAPI ou Firebase)
3. **Étape 3** → Configurer le réseau
4. **Étape 4** → Créer le dashboard
5. **Étape 5** → Ajouter la base de données
6. **Étape 6** → WebSocket (optionnel)

---

## 🔧 Commandes Utiles

### Sur Raspberry Pi
```bash
# Tester la connexion au serveur PC
curl http://192.168.1.100:5000/api/health

# Voir les logs
tail -f logs/smart_bus.log
```

### Sur PC
```bash
# Démarrer Flask
cd server
python app.py

# Démarrer FastAPI
cd server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Voir les données SQLite
sqlite3 data/bus_data.db
SELECT * FROM bus_data ORDER BY timestamp DESC LIMIT 10;
```

---

## 📝 Notes Importantes

- **IP du PC** : Remplacer `192.168.1.100` par l'IP réelle de ton PC
- **Port** : Flask utilise généralement 5000, FastAPI 8000
- **Firewall** : Ne pas oublier d'autoriser le port dans le firewall
- **Pi Connect** : Si tu utilises Pi Connect, la connexion réseau est déjà simplifiée
- **Test** : Toujours tester avec `curl` ou Postman avant d'intégrer dans le code

---

## 🎯 Choix Recommandé selon le Cas

- **Prototype rapide** → Flask + SQLite
- **Production moderne** → FastAPI + SQLite
- **Multi-devices/Cloud** → FastAPI + Firebase Firestore
- **Temps réel avancé** → FastAPI + WebSocket + Firebase

---

**Prêt à commencer ? Choisis ton stack et suis les étapes ! 🚀**

