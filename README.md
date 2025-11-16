# Smart Bus IoT - Projet Raspberry Pi 4

Projet IoT pour un bus intelligent équipé de plusieurs capteurs sur Raspberry Pi 4.

## 📋 Capteurs

- **GPS Neo-6M** : Localisation du bus (connexion UART GPIO)
- **DHT22** : Température et humidité
- **MPU9250** : Accéléromètre, gyroscope et magnétomètre (IMU)
- **2x Ultrasonic (HC-SR04)** : Détection des passagers aux portes d'entrée et de sortie
- **LCD I2C** : Affichage du nombre de passagers en temps réel

## 🏗️ Structure du Projet

```
ProjetPI4/
├── sensors/              # Modules des capteurs
│   ├── __init__.py
│   ├── gps_neo6m.py     # Module GPS
│   ├── dht22.py         # Module température/humidité
│   ├── mpu9250.py       # Module IMU
│   ├── ultrasonic.py    # Module capteur ultrasonique
│   └── lcd.py           # Module afficheur LCD
├── utils/               # Utilitaires
│   ├── __init__.py
│   ├── data_logger.py  # Enregistrement des données
│   └── config_loader.py # Gestion de la configuration
├── config/              # Configuration
│   └── config.json      # Fichier de configuration
├── data/                # Données enregistrées (généré automatiquement)
├── logs/                # Fichiers de log (généré automatiquement)
├── main.py              # Programme principal
├── requirements.txt     # Dépendances Python
└── README.md           # Documentation
```

## 🚀 Installation sur Raspberry Pi 4

### Méthode 1 : Installation automatique (recommandée)

```bash
# Clonez ou copiez le projet sur votre Raspberry Pi
cd ~/ProjetPI4

# Rendez le script exécutable
chmod +x setup.sh

# Lancez l'installation
./setup.sh

# Redémarrez votre Raspberry Pi
sudo reboot
```

### Méthode 2 : Installation manuelle

#### 1. Prérequis

- Raspberry Pi 4 avec Raspberry Pi OS (32-bit ou 64-bit)
- Python 3.7 ou supérieur
- Accès GPIO activé

#### 2. Installation des dépendances système

```bash
# Mise à jour du système
sudo apt-get update
sudo apt-get upgrade -y

# Installation des dépendances système
sudo apt-get install -y python3-pip python3-dev python3-venv
sudo apt-get install -y build-essential git
sudo apt-get install -y i2c-tools
```

#### 3. Activation des interfaces

```bash
# Activation de l'interface I2C (pour MPU9250 et LCD)
sudo raspi-config
# Interface Options → I2C → Enable

# Activation de l'interface série (pour GPS)
# Interface Options → Serial Port → Enable

# Ou en ligne de commande :
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_serial 0
```

#### 4. Installation des dépendances Python

```bash
# Création d'un environnement virtuel (recommandé)
python3 -m venv venv
source venv/bin/activate

# Installation des packages
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Configuration des permissions

```bash
# Ajouter l'utilisateur aux groupes nécessaires
sudo usermod -a -G gpio $USER
sudo usermod -a -G dialout $USER

# Redémarrer pour que les changements prennent effet
sudo reboot
```

#### 6. Configuration

1. Modifiez le fichier `config/config.json` selon votre configuration matérielle
2. Ajustez les numéros de GPIO si nécessaire
3. Vérifiez le port série pour le GPS : `/dev/serial0` (UART GPIO)
4. Vérifiez l'adresse I2C du LCD : `sudo i2cdetect -y 1` (généralement 0x27 ou 0x3F)

## 🔌 Connexions GPIO

Voir le fichier `circuit_ultrasonic.md` pour le schéma complet.

### Résumé des connexions :

- **DHT22** : GPIO 4 (Pin 7)
- **Ultrasonic Entrée** : GPIO 23 (Trig), GPIO 24 (Echo)
- **Ultrasonic Sortie** : GPIO 25 (Trig), GPIO 26 (Echo)
- **MPU9250** : I2C (GPIO 2/SDA, GPIO 3/SCL)
- **LCD I2C** : I2C (GPIO 2/SDA, GPIO 3/SCL) - même bus que MPU9250
- **GPS Neo-6M** : UART GPIO (TX: GPIO 14, RX: GPIO 15) - port `/dev/serial0`

**Note** : Le LCD et le MPU9250 partagent le même bus I2C (c'est normal, ils ont des adresses différentes).

## 🎯 Utilisation

### Lancer le programme principal

```bash
# Si vous utilisez un environnement virtuel
source venv/bin/activate

# Lancer le programme
python3 main.py
```

Le programme va :
1. Initialiser tous les capteurs configurés
2. **Compter automatiquement les passagers** (détection à 3cm)
3. **Afficher sur le LCD** : "Passagers: X/10" ou "BUS PLEIN"
4. Collecter les données à intervalles réguliers
5. Enregistrer les données dans le dossier `data/`
6. Logger les événements dans `logs/smart_bus.log`

### Fonctionnalités principales

- **Comptage automatique de passagers** : Détection à 3cm aux portes d'entrée et de sortie
- **Affichage LCD en temps réel** : Nombre de passagers et statut (PLEIN/occupation)
- **Maximum 10 passagers** : Configurable dans `config/config.json`
- **Enregistrement des données** : Toutes les données sont sauvegardées en JSON/CSV

### Configuration

Modifiez `config/config.json` pour :
- Activer/désactiver des capteurs
- Changer les pins GPIO
- Modifier l'intervalle de collecte
- Changer le format de sauvegarde (JSON/CSV)

## 📊 Format des Données

Les données sont enregistrées au format JSON avec la structure suivante :

```json
{
  "timestamp": "2024-01-01T12:00:00",
  "sensors": {
    "gps": {
      "latitude": 48.8566,
      "longitude": 2.3522,
      "altitude": 35.0,
      "speed": 0.0
    },
    "dht22": {
      "temperature": 22.5,
      "humidity": 45.0,
      "unit": "celsius"
    },
    "mpu9250": {
      "acceleration": {"x": 0.0, "y": 0.0, "z": 9.8},
      "gyroscope": {"x": 0.0, "y": 0.0, "z": 0.0},
      "magnetometer": {"x": 0.0, "y": 0.0, "z": 0.0}
    },
    "ultrasonic_entry": {
      "distance": 25.5,
      "unit": "cm",
      "door_type": "entree",
      "timestamp": 1704110400.0
    },
    "ultrasonic_exit": {
      "distance": 30.0,
      "unit": "cm",
      "door_type": "sortie",
      "timestamp": 1704110400.0
    }
  },
  "passengers": {
    "count": 5,
    "max": 10,
    "is_full": false
  }
}
```

## 🛠️ Développement

### Structure des modules

Chaque capteur a son propre module dans `sensors/` avec :
- Méthode `__init__()` pour l'initialisation
- Méthode `read_data()` pour lire les données
- Méthodes spécifiques pour accéder aux valeurs individuelles

### Ajout d'un nouveau capteur

1. Créez un nouveau fichier dans `sensors/`
2. Implémentez la classe avec `read_data()`
3. Ajoutez l'import dans `sensors/__init__.py`
4. Ajoutez la configuration dans `config/config.json`
5. Intégrez dans `main.py`

## 📝 Notes

- Assurez-vous d'avoir les permissions GPIO (utilisateur dans le groupe `gpio`)
- Le GPS peut prendre quelques minutes pour obtenir un fix satellite
- Certains capteurs nécessitent un temps de stabilisation après l'alimentation
- **DHT22** : Utilise la bibliothèque moderne `adafruit-circuitpython-dht` (compatible avec Raspberry Pi OS Bookworm+)
- **GPS** : Utilise le port série UART GPIO `/dev/serial0` (lien symbolique vers `/dev/ttyAMA0`)

## 🔒 Sécurité

- Ne connectez pas les capteurs avec des tensions incorrectes
- Vérifiez les connexions avant d'alimenter
- Utilisez des résistances de pull-up/pull-down si nécessaire

## 📄 Licence

Ce projet est fourni tel quel pour usage éducatif et de développement.






