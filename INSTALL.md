# Guide d'Installation - Smart Bus IoT sur Raspberry Pi 4

## 📋 Prérequis

- **Raspberry Pi 4** avec Raspberry Pi OS (32-bit ou 64-bit)
- **Carte SD** d'au moins 16 Go (32 Go recommandé)
- **Alimentation** 5V 3A pour Raspberry Pi 4
- **Accès SSH** ou **écran + clavier** pour la configuration

## 🚀 Installation Rapide

### Étape 1 : Préparer votre Raspberry Pi

1. **Installer Raspberry Pi OS** sur la carte SD
2. **Activer SSH** (si vous utilisez un accès distant)
3. **Connecter au réseau** (WiFi ou Ethernet)
4. **Mettre à jour le système** :
   ```bash
   sudo apt-get update
   sudo apt-get upgrade -y
   ```

### Étape 2 : Transférer le projet

**Option A : Via Git (si disponible)**
```bash
cd ~
git clone <votre-repo> ProjetPI4
cd ProjetPI4
```

**Option B : Via SCP (depuis votre ordinateur)**
```bash
# Depuis votre ordinateur Windows/Mac/Linux
scp -r ProjetPI4 pi@<adresse-ip-raspberry>:~/
```

**Option C : Via clé USB**
1. Copiez le dossier `ProjetPI4` sur une clé USB
2. Branchez la clé USB sur le Raspberry Pi
3. Copiez le dossier :
   ```bash
   cp -r /media/pi/<nom-usb>/ProjetPI4 ~/
   cd ~/ProjetPI4
   ```

### Étape 3 : Installation automatique

```bash
cd ~/ProjetPI4
chmod +x setup.sh
./setup.sh
```

Le script va :
- ✅ Mettre à jour le système
- ✅ Installer toutes les dépendances
- ✅ Activer I2C et Serial (UART)
- ✅ Créer l'environnement virtuel
- ✅ Installer les packages Python
- ✅ Créer les dossiers nécessaires
- ✅ Configurer les permissions

### Étape 4 : Redémarrer

```bash
sudo reboot
```

**⚠️ IMPORTANT** : Le redémarrage est nécessaire pour que les interfaces (I2C et UART) soient activées.

### Étape 5 : Vérifier l'installation

Après le redémarrage :

```bash
cd ~/ProjetPI4
source venv/bin/activate

# Vérifier I2C (devrait afficher les adresses des périphériques)
sudo i2cdetect -y 1

# Vérifier le port série GPS
ls -l /dev/serial0

# Tester le programme
python3 main.py
```

## 🔧 Configuration

### 1. Vérifier l'adresse I2C du LCD

```bash
sudo i2cdetect -y 1
```

Vous devriez voir `27` ou `3f` (ou une autre adresse hexadécimale). Si nécessaire, modifiez `config/config.json` :

```json
"lcd": {
  "i2c_address": "0x27",  // Changez selon votre LCD (0x27 ou 0x3F)
  "cols": 16,
  "rows": 2,
  "enabled": true
}
```

### 2. Vérifier le port GPS

Le GPS utilise le port série UART GPIO (`/dev/serial0`). Vérifiez que le port existe :

```bash
ls -l /dev/serial0
```

Si le port n'existe pas, activez l'UART :
```bash
sudo raspi-config
# Interface Options → Serial Port → Enable
# Choisissez "No" pour désactiver le shell login
sudo reboot
```

La configuration par défaut dans `config/config.json` utilise déjà `/dev/serial0`.

### 3. Ajuster les GPIO si nécessaire

Si vous utilisez des pins différents, modifiez `config/config.json` :

```json
"ultrasonic_entry": {
  "trigger_pin": 23,
  "echo_pin": 24,
  "enabled": true
},
"ultrasonic_exit": {
  "trigger_pin": 25,
  "echo_pin": 26,
  "enabled": true
}
```

### 4. Configurer le nombre maximum de passagers

```json
"bus": {
  "max_passengers": 10,
  "detection_threshold": 3.0  // Distance en cm pour détecter un passager
}
```

## ▶️ Lancer le programme

### Mode interactif

```bash
cd ~/ProjetPI4
source venv/bin/activate
python3 main.py
```

Le programme va :
- Initialiser tous les capteurs
- Compter automatiquement les passagers (détection à 3cm)
- Afficher sur le LCD : "Passagers: X/10" ou "BUS PLEIN"
- Enregistrer les données dans `data/`

### Mode service (démarrage automatique)

Créez un service systemd pour lancer automatiquement au démarrage :

```bash
sudo nano /etc/systemd/system/smartbus.service
```

Ajoutez :

```ini
[Unit]
Description=Smart Bus IoT Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ProjetPI4
Environment="PATH=/home/pi/ProjetPI4/venv/bin"
ExecStart=/home/pi/ProjetPI4/venv/bin/python3 /home/pi/ProjetPI4/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activez le service :

```bash
sudo systemctl enable smartbus.service
sudo systemctl start smartbus.service
sudo systemctl status smartbus.service
```

## 🐛 Dépannage

### Problème : "Permission denied" sur GPIO

```bash
sudo usermod -a -G gpio $USER
sudo usermod -a -G dialout $USER
sudo reboot
```

### Problème : LCD non détecté

1. Vérifiez que I2C est activé : `sudo i2cdetect -y 1`
2. Vérifiez les connexions I2C (SDA/SCL)
3. Vérifiez l'alimentation du LCD (5V)
4. Vérifiez l'adresse I2C dans `config/config.json`

### Problème : GPS non détecté

1. Vérifiez que l'UART est activé : `sudo raspi-config` → Serial Port → Enable
2. Vérifiez le port : `ls -l /dev/serial0`
3. Vérifiez les permissions : `sudo usermod -a -G dialout $USER`
4. Vérifiez les connexions (TX GPS → RX Pi GPIO 15, RX GPS → TX Pi GPIO 14)
5. Testez manuellement : `sudo cat /dev/serial0` (devrait afficher des données NMEA)

### Problème : Capteurs ultrason ne fonctionnent pas

1. Vérifiez les connexions VCC (5V) et GND
2. Vérifiez que les pins Trig et Echo sont corrects
3. Vérifiez les distances mesurées dans les logs

### Voir les logs

```bash
tail -f logs/smart_bus.log
```

## ✅ Vérification finale

Avant de lancer le programme, vérifiez que :

- [ ] I2C est activé (`sudo i2cdetect -y 1` fonctionne)
- [ ] UART est activé (`ls -l /dev/serial0` existe)
- [ ] Les dépendances sont installées (`pip list` dans venv)
- [ ] Les dossiers `data/` et `logs/` existent
- [ ] Le fichier `config/config.json` est configuré
- [ ] Les capteurs sont correctement connectés selon `circuit_ultrasonic.md`
- [ ] L'utilisateur est dans les groupes `gpio` et `dialout`

## 🎉 C'est prêt !

Votre Smart Bus IoT est maintenant installé et prêt à compter les passagers !

Pour plus d'informations, consultez :
- `README.md` : Documentation générale
- `circuit_ultrasonic.md` : Schéma de connexion détaillé
