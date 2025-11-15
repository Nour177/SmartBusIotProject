# 🔧 Correction du problème DHT22

## Problème

L'ancienne bibliothèque `Adafruit-Python-DHT` ne fonctionne plus avec les versions modernes de Raspberry Pi OS (Bookworm et plus récentes).

## ✅ Solution appliquée

Le code a été mis à jour pour utiliser la bibliothèque moderne :
- ❌ **Ancienne** : `Adafruit-Python-DHT` (obsolète)
- ✅ **Nouvelle** : `adafruit-circuitpython-dht` + `adafruit-blinka` (maintenue)

## 📝 Instructions de réinstallation

### Option 1 : Réinstallation complète (recommandée)

```bash
cd ~/ProjetPI4

# Activer l'environnement virtuel si vous l'utilisez
source venv/bin/activate

# Désinstaller l'ancienne bibliothèque (si installée)
pip uninstall Adafruit-Python-DHT -y

# Installer les nouvelles bibliothèques
pip install adafruit-circuitpython-dht>=2.4.4
pip install adafruit-blinka>=8.0.0

# Ou réinstaller toutes les dépendances
pip install -r requirements.txt
```

### Option 2 : Mise à jour depuis requirements.txt

```bash
cd ~/ProjetPI4
source venv/bin/activate

# Mettre à jour requirements.txt (déjà fait)
# Puis réinstaller
pip install -r requirements.txt --upgrade
```

## ✅ Vérification

Testez que le DHT22 fonctionne :

```bash
cd ~/ProjetPI4
source venv/bin/activate
python3 -c "from sensors.dht22 import DHT22; dht = DHT22(4); print(dht.read_data())"
```

Vous devriez voir quelque chose comme :
```python
{'temperature': 22.5, 'humidity': 45.0, 'unit': 'celsius'}
```

## 🚀 Lancer le programme

Une fois la réinstallation terminée :

```bash
cd ~/ProjetPI4
source venv/bin/activate
python3 main.py
```

## 📌 Notes importantes

1. **Blinka** : La nouvelle bibliothèque utilise `adafruit-blinka` qui gère les GPIO de manière moderne
2. **Compatible** : Cette bibliothèque fonctionne avec Raspberry Pi OS Bookworm et les versions plus récentes
3. **Performance** : La nouvelle bibliothèque est plus stable et mieux maintenue

## 🐛 Si vous avez encore des problèmes

### Erreur : "No module named 'board'"

```bash
pip install adafruit-blinka
```

### Erreur : "No module named 'adafruit_dht'"

```bash
pip install adafruit-circuitpython-dht
```

### Erreur de permissions GPIO

```bash
sudo usermod -a -G gpio $USER
sudo reboot
```

### Vérifier que Blinka détecte bien le Raspberry Pi

```bash
python3 -c "import board; print('Board détecté:', board.board_id)"
```

Vous devriez voir : `Board détecté: RASPBERRY_PI_4B` (ou similaire)

