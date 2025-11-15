#!/bin/bash

# Script de correction rapide pour installer les dépendances manquantes

echo "=== Correction des dépendances Smart Bus IoT ==="
echo ""

# Vérifier si on est dans l'environnement virtuel
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Activation de l'environnement virtuel..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "❌ Environnement virtuel non trouvé. Créez-le d'abord :"
        echo "   python3 -m venv venv"
        echo "   source venv/bin/activate"
        exit 1
    fi
fi

echo "✅ Environnement virtuel activé"
echo ""

# Mise à jour de pip
echo "📦 Mise à jour de pip..."
pip install --upgrade pip

echo ""
echo "📦 Installation des dépendances manquantes..."
echo ""

# Installation des dépendances une par une avec messages
echo "1. GPS (pyserial, pynmea2)..."
pip install pyserial>=3.5 pynmea2>=1.19.0

echo "2. DHT22 (adafruit-circuitpython-dht, adafruit-blinka)..."
pip install adafruit-circuitpython-dht>=2.4.4 adafruit-blinka>=8.0.0

echo "3. MPU9250 (mpu9250-jmdev)..."
pip install mpu9250-jmdev>=1.0.0

echo "4. GPIO (RPi.GPIO)..."
pip install RPi.GPIO>=0.7.1

echo "5. LCD (RPLCD)..."
pip install RPLCD>=0.9.0

echo "6. Utilitaires (python-dotenv)..."
pip install python-dotenv>=1.0.0

echo ""
echo "=== Vérification des installations ==="
echo ""

# Vérifier les installations
python3 -c "import serial; print('✅ pyserial')" 2>/dev/null || echo "❌ pyserial"
python3 -c "import pynmea2; print('✅ pynmea2')" 2>/dev/null || echo "❌ pynmea2"
python3 -c "import adafruit_dht; print('✅ adafruit-circuitpython-dht')" 2>/dev/null || echo "❌ adafruit-circuitpython-dht"
python3 -c "import board; print('✅ adafruit-blinka')" 2>/dev/null || echo "❌ adafruit-blinka"
python3 -c "import mpu9250_jmdev; print('✅ mpu9250-jmdev')" 2>/dev/null || echo "❌ mpu9250-jmdev"
python3 -c "import RPi.GPIO; print('✅ RPi.GPIO')" 2>/dev/null || echo "❌ RPi.GPIO"
python3 -c "from RPLCD.i2c import CharLCD; print('✅ RPLCD')" 2>/dev/null || echo "❌ RPLCD"
python3 -c "import dotenv; print('✅ python-dotenv')" 2>/dev/null || echo "❌ python-dotenv"

echo ""
echo "=== Correction terminée ==="
echo ""
echo "📌 Vérifiez aussi :"
echo "   1. Que l'UART est activé : sudo raspi-config → Serial Port → Enable"
echo "   2. Que I2C est activé : sudo raspi-config → I2C → Enable"
echo "   3. Que le port GPS est correct dans config/config.json : /dev/ttyAMA0"
echo "   4. Redémarrez si nécessaire : sudo reboot"
echo ""

