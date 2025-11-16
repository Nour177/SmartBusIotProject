#!/bin/bash

# Script d'installation pour Smart Bus IoT
# À exécuter sur Raspberry Pi 4

echo "=== Installation Smart Bus IoT ==="

# Mise à jour du système
echo "Mise à jour du système..."
sudo apt-get update
sudo apt-get upgrade -y

# Installation des dépendances système
echo "Installation des dépendances système..."
sudo apt-get install -y python3-pip python3-dev python3-venv
sudo apt-get install -y build-essential git
sudo apt-get install -y i2c-tools

# Activation de l'interface I2C (pour MPU9250 et LCD)
echo "Activation de l'interface I2C..."
sudo raspi-config nonint do_i2c 0

# Activation de l'interface série UART (pour GPS Neo-6M via GPIO)
echo "Activation de l'interface série UART pour GPS..."
sudo raspi-config nonint do_serial 0
echo "UART activé - Le GPS utilisera /dev/serial0"

# Création de l'environnement virtuel
echo "Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

# Installation des dépendances Python
echo "Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Création des dossiers nécessaires
echo "Création des dossiers..."
mkdir -p data
mkdir -p logs
mkdir -p config

# Permissions
echo "Configuration des permissions..."
sudo usermod -a -G gpio $USER
sudo usermod -a -G dialout $USER

echo ""
echo "=== Installation terminée ==="
echo ""
echo "✅ Interfaces activées :"
echo "   - I2C (pour MPU9250 et LCD)"
echo "   - UART série (pour GPS Neo-6M sur /dev/serial0)"
echo ""
echo "⚠️  IMPORTANT : Redémarrez votre Raspberry Pi pour que les changements prennent effet :"
echo "   sudo reboot"
echo ""
echo "Après le redémarrage :"
echo "   1. Activez l'environnement virtuel : source venv/bin/activate"
echo "   2. Vérifiez la configuration dans config/config.json"
echo "   3. Lancez le programme : python3 main.py"
echo ""
echo "📌 Note : Le GPS se connecte via UART GPIO (TX: GPIO 14, RX: GPIO 15)"
echo "   Port série : /dev/serial0"
echo ""






