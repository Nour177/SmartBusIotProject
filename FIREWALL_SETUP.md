# 🔥 Configuration du Firewall Windows
## Autoriser les connexions depuis la Raspberry Pi

---

## 🎯 Objectif

Autoriser le port **8000** (FastAPI) pour recevoir les données de la Raspberry Pi.

---

## 📋 Méthode 1 : Interface Graphique (Recommandée)

### Étape 1 : Ouvrir le Pare-feu Windows Defender

1. Appuie sur **Windows + R**
2. Tape `wf.msc` et appuie sur **Entrée**
   - Ou cherche "Pare-feu Windows Defender avec sécurité avancée" dans le menu Démarrer

### Étape 2 : Créer une Règle Entrante

1. Dans le panneau de gauche, clique sur **Règles de trafic entrant**
2. Dans le panneau de droite, clique sur **Nouvelle règle...**

### Étape 3 : Configurer la Règle

1. **Type de règle** : Sélectionne **Port** → **Suivant**
2. **Protocole et ports** :
   - Sélectionne **TCP**
   - Sélectionne **Ports locaux spécifiques**
   - Tape `8000` dans le champ
   - Clique sur **Suivant**
3. **Action** : Sélectionne **Autoriser la connexion** → **Suivant**
4. **Profil** : Coche toutes les cases (Domaine, Privé, Public) → **Suivant**
5. **Nom** : Donne un nom à la règle (ex: "FastAPI Smart Bus Port 8000")
6. Clique sur **Terminer**

### ✅ Vérification

La règle devrait maintenant apparaître dans la liste des **Règles de trafic entrant**.

---

## 📋 Méthode 2 : Ligne de Commande (PowerShell en Administrateur)

### Étape 1 : Ouvrir PowerShell en Administrateur

1. Clique droit sur **PowerShell** dans le menu Démarrer
2. Sélectionne **Exécuter en tant qu'administrateur**

### Étape 2 : Créer la Règle

Exécute cette commande :

```powershell
New-NetFirewallRule -DisplayName "FastAPI Smart Bus Port 8000" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### ✅ Vérification

Vérifie que la règle a été créée :

```powershell
Get-NetFirewallRule -DisplayName "FastAPI Smart Bus Port 8000"
```

---

## 📋 Méthode 3 : Autoriser une Application (Alternative)

Si tu préfères autoriser Python/FastAPI directement :

### Étape 1 : Ouvrir le Pare-feu Windows Defender

1. Appuie sur **Windows + R**
2. Tape `firewall.cpl` et appuie sur **Entrée**

### Étape 2 : Autoriser une Application

1. Clique sur **Autoriser une application ou une fonctionnalité via le Pare-feu Windows**
2. Clique sur **Modifier les paramètres** (en haut à droite)
3. Clique sur **Autoriser une autre application...**
4. Clique sur **Parcourir...**
5. Navigue vers ton environnement Python :
   - Exemple : `C:\Users\LENOVO\AppData\Local\Programs\Python\Python3xx\python.exe`
   - Ou : `C:\Users\LENOVO\venv\Scripts\python.exe` (si tu utilises un venv)
6. Clique sur **Ajouter**
7. Coche **Privé** et **Public**
8. Clique sur **OK**

---

## 🧪 Test de la Configuration

### Test 1 : Depuis la Raspberry Pi

```bash
# Teste la connexion HTTP (remplace par l'IP réelle du PC)
curl http://192.168.1.100:8000/api/health
```

### Test 2 : Depuis le PC (local)

```powershell
# Teste si le port est ouvert
Test-NetConnection -ComputerName localhost -Port 8000
```

### Test 3 : Vérifier que le serveur FastAPI écoute

Assure-toi que ton serveur FastAPI est démarré :

```bash
# Dans le dossier server/
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le paramètre `--host 0.0.0.0` est important pour accepter les connexions depuis d'autres machines.

---

## 🔍 Vérifier les Règles Existantes

### Via Interface Graphique

1. Ouvre **Pare-feu Windows Defender avec sécurité avancée**
2. Clique sur **Règles de trafic entrant**
3. Cherche ta règle dans la liste

### Via PowerShell

```powershell
# Voir toutes les règles pour le port 8000
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*8000*"}

# Voir les règles actives
Get-NetFirewallRule | Where-Object {$_.Enabled -eq $true} | Select-Object DisplayName, Direction, Action
```

---

## 🗑️ Supprimer une Règle (si nécessaire)

### Via Interface Graphique

1. Ouvre **Pare-feu Windows Defender avec sécurité avancée**
2. Clique sur **Règles de trafic entrant**
3. Trouve ta règle, clique droit → **Supprimer**

### Via PowerShell

```powershell
# Supprimer une règle par nom
Remove-NetFirewallRule -DisplayName "FastAPI Smart Bus Port 8000"
```

---

## ⚠️ Notes Importantes

1. **Host 0.0.0.0** : Assure-toi que FastAPI écoute sur `0.0.0.0` et non `127.0.0.1`
   ```python
   # Dans server/main.py ou la commande uvicorn
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Réseau Privé vs Public** : 
   - Si tu es sur un réseau **Privé** (maison), autorise au moins **Privé**
   - Si tu es sur un réseau **Public** (café, etc.), autorise **Public** (moins sécurisé)

3. **Antivirus** : Certains antivirus peuvent aussi bloquer les connexions. Vérifie les paramètres de ton antivirus si le problème persiste.

4. **Routeur/Firewall** : Si le problème persiste, vérifie aussi les paramètres du routeur.

---

## 🎯 Configuration Recommandée pour le Développement

Pour le développement local, autorise :
- ✅ **Port 8000** (FastAPI)
- ✅ **Réseau Privé** (si tu es chez toi)
- ✅ **Réseau Public** (si nécessaire, mais moins sécurisé)

---

## 📝 Commandes Utiles

### Voir toutes les règles actives
```powershell
Get-NetFirewallRule | Where-Object {$_.Enabled -eq $true} | Format-Table DisplayName, Direction, Action
```

### Voir les ports ouverts
```powershell
Get-NetFirewallPortFilter | Where-Object {$_.LocalPort -eq 8000}
```

### Tester la connectivité
```powershell
# Depuis le PC
Test-NetConnection -ComputerName localhost -Port 8000

# Depuis la Raspberry Pi (remplace par l'IP du PC)
curl -v http://192.168.1.100:8000/api/health
```

---

**Une fois la règle créée, teste la connexion depuis la Raspberry Pi ! 🚀**

