"""
Module GPS Neo-6M pour la localisation du bus
"""

import serial
import pynmea2
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class GPSNeo6M:
    """Classe pour gérer le module GPS Neo-6M"""
    
    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 9600):
        """
        Initialise le module GPS
        
        Args:
            port: Port série (par défaut /dev/ttyUSB0)
            baudrate: Vitesse de communication (par défaut 9600)
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.speed = None
        self.timestamp = None
        
    def connect(self) -> bool:
        """Établit la connexion série avec le module GPS"""
        try:
            self.serial_connection = serial.Serial(
                self.port,
                self.baudrate,
                timeout=1
            )
            logger.info(f"GPS connecté sur {self.port}")
            return True
        except Exception as e:
            logger.error(f"Erreur de connexion GPS: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion série"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logger.info("GPS déconnecté")
    
    def read_data(self) -> Optional[Dict]:
        """
        Lit les données GPS depuis le module
        
        Returns:
            Dictionnaire contenant les données GPS ou None en cas d'erreur
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            if not self.connect():
                return None
        
        try:
            line = self.serial_connection.readline().decode('utf-8', errors='ignore')
            if line.startswith('$GPRMC') or line.startswith('$GPGGA'):
                msg = pynmea2.parse(line)
                
                if isinstance(msg, pynmea2.types.talker.RMC):
                    if msg.latitude and msg.longitude:
                        self.latitude = float(msg.latitude)
                        self.longitude = float(msg.longitude)
                        self.speed = float(msg.spd_over_grnd) if msg.spd_over_grnd else 0.0
                        self.timestamp = msg.timestamp
                
                elif isinstance(msg, pynmea2.types.talker.GGA):
                    if msg.latitude and msg.longitude:
                        self.latitude = float(msg.latitude)
                        self.longitude = float(msg.longitude)
                        self.altitude = float(msg.altitude) if msg.altitude else None
                
                return {
                    'latitude': self.latitude,
                    'longitude': self.longitude,
                    'altitude': self.altitude,
                    'speed': self.speed,
                    'timestamp': str(self.timestamp) if self.timestamp else None
                }
        except Exception as e:
            logger.error(f"Erreur lecture GPS: {e}")
            return None
        
        return None
    
    def get_position(self) -> Optional[Dict]:
        """Retourne la position actuelle"""
        return self.read_data()






