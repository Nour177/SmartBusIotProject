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

# Activation de l'interface I2C
echo "Activation de l'interface I2C..."
sudo raspi-config nonint do_i2c 0

# Activation de l'interface série pour GPS
echo "Activation de l'interface série..."
sudo raspi-config nonint do_serial 0

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

echo "=== Installation terminée ==="
echo "Veuillez redémarrer votre Raspberry Pi pour que les changements prennent effet."
echo "Ensuite, activez l'environnement virtuel avec: source venv/bin/activate"
echo "Et lancez le programme avec: python3 main.py"






