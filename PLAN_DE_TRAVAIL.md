# 📋 Plan de Travail - Smart Bus IoT
## Communication Raspberry Pi → PC avec FastAPI + Firebase Firestore

---

## 🎯 Vue d'ensemble

**Objectif** : Créer un système complet où la Raspberry Pi envoie les données des capteurs au PC via FastAPI, qui les stocke dans Firebase Firestore et les affiche dans un dashboard web.

**Stack Technique Choisi** :
- ✅ **FastAPI** : API moderne, performante, avec documentation automatique
- ✅ **Firebase Firestore** : Base de données cloud, scalable, temps réel intégré
- ✅ **Dashboard HTML** : Interface web avec Chart.js

---

## 🔄 Étapes du Plan de Travail

### **ÉTAPE 1 : Préparer la Raspberry Pi**
- [ ] Vérifier que tous les capteurs fonctionnent (`python3 main.py`)
- [ ] Installer `requests` pour les requêtes HTTP
  ```bash
  pip install requests
  ```
- [ ] Ajouter la configuration du serveur PC dans `config/config.json`
  ```json
  "server": {
    "enabled": true,
    "url": "http://192.168.1.100:8000",
    "timeout": 5,
    "retry_count": 3,
    "bus_id": "Bus1"
  }
  ```
- [ ] Créer un module `utils/http_client.py` pour envoyer les données
- [ ] Modifier `main.py` pour intégrer l'envoi HTTP POST après chaque collecte

**Livrable** : Raspberry Pi envoie des JSON au PC via HTTP POST

---

### **ÉTAPE 2 : Configurer Firebase Firestore**

#### **2.1 : Créer un projet Firebase**
- [ ] Aller sur [Firebase Console](https://console.firebase.google.com/)
- [ ] Créer un nouveau projet (ex: "SmartBusIoT")
- [ ] Activer **Firestore Database**
- [ ] Choisir le mode **Production** (ou Test pour développement)
- [ ] Choisir une région (ex: `europe-west1`)

#### **2.2 : Obtenir les credentials**
- [ ] Aller dans **Project Settings** → **Service Accounts**
- [ ] Cliquer sur **Generate New Private Key**
- [ ] Télécharger le fichier JSON (ex: `smartbus-firebase-adminsdk.json`)
- [ ] **⚠️ IMPORTANT** : Ne jamais commiter ce fichier dans Git !

#### **2.3 : Configurer les règles Firestore (optionnel)**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /bus_data/{document=**} {
      allow read: if true;  // Public read pour le dashboard
      allow write: if request.auth != null;  // Write seulement si authentifié
    }
  }
}
```

**Livrable** : Projet Firebase créé avec Firestore activé

---

### **ÉTAPE 3 : Installer FastAPI sur PC**

#### **3.1 : Installation des dépendances**
- [ ] Créer un environnement virtuel (recommandé)
  ```bash
  python -m venv venv
  # Windows
  venv\Scripts\activate
  # Linux/Mac
  source venv/bin/activate
  ```
- [ ] Installer FastAPI et Firebase
  ```bash
  pip install fastapi uvicorn[standard] python-multipart
  pip install firebase-admin
  pip install python-dotenv
  ```

#### **3.2 : Structure du projet serveur**
```
server/
├── main.py              # Application FastAPI principale
├── firebase_config.py    # Configuration Firebase
├── models.py            # Modèles de données (Pydantic)
├── dashboard/
│   └── index.html       # Dashboard web
├── .env                 # Variables d'environnement (credentials Firebase)
├── requirements.txt     # Dépendances
└── .gitignore          # Ignorer .env et credentials
```

#### **3.3 : Créer l'application FastAPI**
- [ ] Créer `server/main.py` avec FastAPI
- [ ] Endpoints à créer :
  - `POST /api/data` - Recevoir les données de la Pi
  - `GET /api/latest` - Dernière donnée depuis Firestore
  - `GET /api/history` - Historique des données
  - `GET /api/health` - Vérifier que le serveur fonctionne
  - `GET /` - Rediriger vers le dashboard
- [ ] Documentation automatique sur `http://localhost:8000/docs`

**Livrable** : Serveur FastAPI fonctionnel sur PC (port 8000)

---

### **ÉTAPE 4 : Intégrer Firebase Firestore**

#### **4.1 : Configuration Firebase**
- [ ] Créer `server/firebase_config.py` pour initialiser Firebase
- [ ] Placer le fichier JSON des credentials dans `server/` (ex: `smartbus-firebase-adminsdk.json`)
- [ ] Créer `.env` pour stocker le chemin du fichier (optionnel)
  ```env
  FIREBASE_CREDENTIALS_PATH=smartbus-firebase-adminsdk.json
  ```

#### **4.2 : Structure Firestore**
- [ ] Créer une collection `bus_data` dans Firestore
- [ ] Structure d'un document :
  ```json
  {
    "timestamp": "2025-11-17T10:00:00",
    "bus_id": "Bus1",
    "data": {
      "sensors": {...},
      "passengers": {...}
    },
    "created_at": "2025-11-17T10:00:00"
  }
  ```

#### **4.3 : Implémenter les opérations Firestore**
- [ ] Dans `POST /api/data` : Écrire les données dans Firestore
- [ ] Dans `GET /api/latest` : Lire la dernière donnée depuis Firestore
- [ ] Dans `GET /api/history` : Lire l'historique avec filtres (date, bus_id)

**Livrable** : Données stockées et récupérables depuis Firebase Firestore

---

### **ÉTAPE 5 : Configuration Réseau (Raspberry → PC)**

- [ ] Trouver l'IP locale du PC
  - Windows : `ipconfig` → IPv4 Address
  - Linux/Mac : `ifconfig` ou `ip addr`
- [ ] Vérifier que Raspberry Pi et PC sont sur le même réseau
- [ ] Tester la connectivité depuis la Pi
  ```bash
  ping 192.168.1.100  # Remplacer par l'IP du PC
  ```
- [ ] Configurer le firewall du PC pour autoriser le port 8000
  - Windows : Règle de pare-feu entrante pour le port 8000
  - Linux : `sudo ufw allow 8000`
- [ ] Mettre à jour l'URL dans `config/config.json` de la Pi
  ```json
  "url": "http://192.168.1.100:8000"
  ```

**Livrable** : Communication réseau établie entre Pi et PC

---

### **ÉTAPE 6 : Dashboard HTML avec Temps Réel**

- [ ] Créer `server/dashboard/index.html`
- [ ] Intégrer Chart.js pour les graphiques
  ```html
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  ```
- [ ] Créer une fonction JavaScript qui appelle `/api/latest` toutes les 2-5 secondes
- [ ] Afficher :
  - Nombre de passagers (avec barre de progression)
  - GPS (latitude, longitude, vitesse, statut fix)
  - Température et humidité
  - Accélération (X, Y, Z)
  - Graphiques en temps réel
- [ ] Ajouter un indicateur de statut (en ligne/hors ligne)
- [ ] Optionnel : Utiliser Firebase Realtime Database pour les mises à jour instantanées

**Livrable** : Dashboard web fonctionnel accessible sur `http://localhost:8000`

---

### **ÉTAPE 7 : WebSocket pour Temps Réel (Optionnel mais Recommandé)**

- [ ] FastAPI supporte WebSocket nativement
- [ ] Créer un endpoint WebSocket dans FastAPI
  ```python
  @app.websocket("/ws")
  async def websocket_endpoint(websocket: WebSocket):
      await websocket.accept()
      # Envoyer les nouvelles données automatiquement
  ```
- [ ] Modifier le dashboard pour utiliser WebSocket au lieu de polling
- [ ] Écouter les changements Firestore en temps réel (Firebase SDK côté serveur)
- [ ] Diffuser les nouvelles données à tous les clients connectés

**Livrable** : Mise à jour en temps réel sans polling

---

## 🚀 Ordre d'Exécution Recommandé

1. **Étape 1** → Préparer la Raspberry Pi
2. **Étape 2** → Configurer Firebase Firestore
3. **Étape 3** → Installer FastAPI sur PC
4. **Étape 4** → Intégrer Firebase Firestore dans FastAPI
5. **Étape 5** → Configurer le réseau
6. **Étape 6** → Créer le dashboard
7. **Étape 7** → WebSocket pour temps réel (optionnel)

---

## 🔧 Commandes Utiles

### Sur Raspberry Pi
```bash
# Tester la connexion au serveur PC
curl http://192.168.1.100:8000/api/health

# Voir les logs
tail -f logs/smart_bus.log

# Tester l'envoi de données
curl -X POST http://192.168.1.100:8000/api/data \
  -H "Content-Type: application/json" \
  -d '{"bus_id":"Bus1","timestamp":"2025-11-17T10:00:00","sensors":{}}'
```

### Sur PC
```bash
# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Démarrer FastAPI
cd server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Accéder à la documentation API
# http://localhost:8000/docs

# Accéder au dashboard
# http://localhost:8000
```

### Firebase Firestore
```bash
# Voir les données dans Firebase Console
# https://console.firebase.google.com/
# → Firestore Database → bus_data collection
```

---

## 📝 Notes Importantes

- **IP du PC** : Remplacer `192.168.1.100` par l'IP réelle de ton PC
- **Port** : FastAPI utilise le port 8000 par défaut
- **Firewall** : Ne pas oublier d'autoriser le port 8000 dans le firewall
- **Firebase Credentials** : ⚠️ **NE JAMAIS** commiter le fichier JSON des credentials dans Git !
- **Pi Connect** : Si tu utilises Pi Connect, la connexion réseau est déjà simplifiée
- **Test** : Toujours tester avec `curl` ou Postman avant d'intégrer dans le code
- **Documentation API** : FastAPI génère automatiquement la documentation sur `/docs`

---

## 🔐 Sécurité Firebase

### Fichiers à ignorer dans Git
Créer un `.gitignore` dans `server/` :
```
.env
*.json
!package.json
__pycache__/
*.pyc
venv/
```

### Variables d'environnement
Utiliser `.env` pour stocker les chemins sensibles :
```env
FIREBASE_CREDENTIALS_PATH=smartbus-firebase-adminsdk.json
FIREBASE_PROJECT_ID=smartbus-iot
```

---

## 🎯 Avantages de FastAPI + Firebase

- ✅ **FastAPI** : API moderne, rapide, documentation automatique
- ✅ **Firebase Firestore** : 
  - Pas besoin d'installer une base de données locale
  - Accès depuis n'importe où (cloud)
  - Scalable automatiquement
  - Temps réel intégré
  - Gratuit jusqu'à 50K lectures/jour
- ✅ **Multi-devices** : Plusieurs Raspberry Pi peuvent envoyer au même Firebase
- ✅ **Dashboard accessible** : Le dashboard peut être hébergé n'importe où

---

## 📊 Structure des Données Firestore

### Collection : `bus_data`
```json
{
  "id": "auto-generated",
  "timestamp": "2025-11-17T10:00:00",
  "bus_id": "Bus1",
  "data": {
    "sensors": {
      "gps": {...},
      "dht22": {...},
      "mpu9250": {...},
      "ultrasonic_entry": {...},
      "ultrasonic_exit": {...}
    },
    "passengers": {
      "count": 3,
      "max": 5,
      "is_full": false
    }
  },
  "created_at": "2025-11-17T10:00:00"
}
```

### Index Firestore recommandés
- `timestamp` (descending)
- `bus_id` + `timestamp` (composite)

---

**Prêt à commencer ? Suis les étapes dans l'ordre ! 🚀**
