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
    
    def __init__(self, port: str = '/dev/serial0', baudrate: int = 9600):
        """
        Initialise le module GPS
        
        Args:
            port: Port série UART GPIO (par défaut /dev/serial0 pour Raspberry Pi)
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
        Lit plusieurs lignes pour augmenter les chances de trouver des données valides
        
        Returns:
            Dictionnaire contenant les données GPS ou None en cas d'erreur
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            if not self.connect():
                return None
        
        try:
            # Lire plusieurs lignes pour augmenter les chances de trouver des données valides
            data_found = False
            max_attempts = 10  # Lire jusqu'à 10 lignes
            
            for _ in range(max_attempts):
                if self.serial_connection.in_waiting == 0:
                    break
                    
                line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                
                if not line or len(line) < 10:
                    continue
                
                # Traiter les messages GPRMC (Recommandé Minimum)
                if line.startswith('$GPRMC'):
                    try:
                        msg = pynmea2.parse(line)
                        if isinstance(msg, pynmea2.types.talker.RMC):
                            # Vérifier si le GPS a un fix (status 'A' = Active, 'V' = Void)
                            if msg.status == 'A' and msg.latitude and msg.longitude:
                                self.latitude = float(msg.latitude)
                                self.longitude = float(msg.longitude)
                                self.speed = float(msg.spd_over_grnd) * 1.852 if msg.spd_over_grnd else 0.0  # Convertir nœuds en km/h
                                self.timestamp = msg.timestamp
                                data_found = True
                    except Exception as e:
                        logger.debug(f"Erreur parsing GPRMC: {e}")
                        continue
                
                # Traiter les messages GPGGA (Global Positioning System Fix Data)
                elif line.startswith('$GPGGA'):
                    try:
                        msg = pynmea2.parse(line)
                        if isinstance(msg, pynmea2.types.talker.GGA):
                            # Vérifier la qualité du fix (0 = pas de fix, 1-2 = fix GPS)
                            if msg.gps_qual > 0 and msg.latitude and msg.longitude:
                                self.latitude = float(msg.latitude)
                                self.longitude = float(msg.longitude)
                                self.altitude = float(msg.altitude) if msg.altitude else None
                                data_found = True
                    except Exception as e:
                        logger.debug(f"Erreur parsing GPGGA: {e}")
                        continue
            
            # Retourner les données si on a trouvé quelque chose, ou les dernières données connues
            if data_found or (self.latitude is not None and self.longitude is not None):
                return {
                    'latitude': self.latitude,
                    'longitude': self.longitude,
                    'altitude': self.altitude,
                    'speed': self.speed if self.speed is not None else 0.0,
                    'timestamp': str(self.timestamp) if self.timestamp else None,
                    'has_fix': data_found
                }
            else:
                # Pas de fix GPS pour le moment
                return {
                    'latitude': None,
                    'longitude': None,
                    'altitude': None,
                    'speed': 0.0,
                    'timestamp': None,
                    'has_fix': False,
                    'status': 'En attente de fix satellite...'
                }
                
        except Exception as e:
            logger.error(f"Erreur lecture GPS: {e}")
            return None
    
    def get_position(self) -> Optional[Dict]:
        """Retourne la position actuelle"""
        return self.read_data()








