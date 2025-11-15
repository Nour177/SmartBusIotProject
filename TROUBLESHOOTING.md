# 🔧 Guide de Dépannage - Smart Bus IoT

## Problèmes courants et solutions

### ❌ Erreur GPS : `could not open port /dev/ttyUSB0`

**Problème** : Le GPS essaie d'utiliser `/dev/ttyUSB0` au lieu de `/dev/ttyAMA0`

**Solutions** :

1. **Vérifier la configuration** :
   ```bash
   cat config/config.json | grep -A 3 gps
   ```
   Le port doit être `/dev/ttyAMA0`

2. **Corriger manuellement** :
   ```bash
   nano config/config.json
   ```
   Changez `"port": "/dev/ttyUSB0"` en `"port": "/dev/ttyAMA0"`

3. **Vérifier que l'UART est activé** :
   ```bash
   sudo raspi-config
   # Interface Options → Serial Port → Enable
   ```

4. **Vérifier que le port existe** :
   ```bash
   ls -l /dev/ttyAMA0
   ```
   Si le fichier n'existe pas, redémarrez : `sudo reboot`

5. **Tester la connexion GPS** :
   ```bash
   sudo cat /dev/ttyAMA0
   ```
   Vous devriez voir des lignes NMEA (commençant par `$GPRMC`, `$GPGGA`, etc.)

---

### ⚠️ WARNING: mpu9250_jmdev non disponible

**Problème** : La bibliothèque MPU9250 n'est pas installée

**Solution** :
```bash
source venv/bin/activate
pip install mpu9250-jmdev
```

Ou réinstaller toutes les dépendances :
```bash
pip install -r requirements.txt
```

---

### ⚠️ WARNING: Bibliothèque LCD non disponible

**Problème** : La bibliothèque RPLCD n'est pas installée

**Solution** :
```bash
source venv/bin/activate
pip install RPLCD
```

Ou réinstaller toutes les dépendances :
```bash
pip install -r requirements.txt
```

---

### ⚠️ WARNING: Impossible de lire les données du DHT22

**Problèmes possibles** :

1. **Bibliothèque non installée** :
   ```bash
   source venv/bin/activate
   pip install adafruit-circuitpython-dht adafruit-blinka
   ```

2. **Mauvais pin GPIO** :
   - Vérifiez dans `config/config.json` que le pin est correct (par défaut GPIO 4)
   - Vérifiez les connexions physiques

3. **Permissions GPIO** :
   ```bash
   sudo usermod -a -G gpio $USER
   sudo reboot
   ```

4. **DHT22 nécessite un temps de stabilisation** :
   - Attendez quelques secondes après le démarrage
   - Le DHT22 peut nécessiter plusieurs tentatives

5. **Vérifier les connexions** :
   - VCC → 3.3V ou 5V
   - GND → GND
   - DATA → GPIO 4 (avec résistance pull-up 4.7kΩ-10kΩ)

---

### ❌ Erreur : Permission denied sur GPIO

**Solution** :
```bash
sudo usermod -a -G gpio $USER
sudo usermod -a -G dialout $USER
sudo reboot
```

---

### ❌ Erreur : Port série non trouvé

**Pour GPS UART** :
```bash
# Vérifier que l'UART est activé
sudo raspi-config
# Interface Options → Serial Port → Enable

# Vérifier le port
ls -l /dev/ttyAMA0

# Si le port n'existe pas, redémarrer
sudo reboot
```

---

### ❌ Erreur : I2C non détecté

**Pour MPU9250 et LCD** :
```bash
# Activer I2C
sudo raspi-config
# Interface Options → I2C → Enable

# Vérifier la détection
sudo i2cdetect -y 1

# Vous devriez voir :
# - 0x68 ou 0x69 pour MPU9250
# - 0x27 ou 0x3F pour LCD
```

---

### 📋 Checklist de vérification

Avant de lancer le programme, vérifiez :

- [ ] Toutes les dépendances sont installées : `pip list`
- [ ] I2C est activé : `sudo i2cdetect -y 1`
- [ ] UART est activé : `ls -l /dev/ttyAMA0`
- [ ] Permissions GPIO : `groups` (doit contenir `gpio` et `dialout`)
- [ ] Configuration correcte : `cat config/config.json`
- [ ] Port GPS correct : `/dev/ttyAMA0` (pas `/dev/ttyUSB0`)
- [ ] Capteurs correctement connectés selon `circuit_ultrasonic.md`

---

### 🔄 Réinstallation complète des dépendances

Si vous avez des problèmes persistants :

```bash
cd ~/ProjetPI4
source venv/bin/activate

# Désinstaller toutes les dépendances
pip freeze | xargs pip uninstall -y

# Réinstaller
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 📞 Informations de débogage

Pour obtenir plus d'informations :

```bash
# Voir les logs en temps réel
tail -f logs/smart_bus.log

# Tester chaque capteur individuellement
python3 -c "from sensors.dht22 import DHT22; dht = DHT22(4); print(dht.read_data())"
python3 -c "from sensors.gps_neo6m import GPSNeo6M; gps = GPSNeo6M('/dev/ttyAMA0'); gps.connect(); print(gps.read_data())"
```

---

### 🆘 Si rien ne fonctionne

1. Vérifiez que vous êtes dans l'environnement virtuel : `source venv/bin/activate`
2. Vérifiez la version de Python : `python3 --version` (doit être 3.7+)
3. Vérifiez la version de Raspberry Pi OS : `cat /etc/os-release`
4. Redémarrez le Raspberry Pi : `sudo reboot`
5. Relancez le script d'installation : `./setup.sh`

