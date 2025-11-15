"""
Module DHT22 pour la mesure de température et d'humidité
Utilise la bibliothèque moderne adafruit-circuitpython-dht
"""

import board
import adafruit_dht
from typing import Optional, Dict
import logging
import time

logger = logging.getLogger(__name__)

# Mapping des pins GPIO aux pins board
PIN_MAPPING = {
    4: board.D4,
    18: board.D18,
    17: board.D17,
    27: board.D27,
    22: board.D22,
    23: board.D23,
    24: board.D24,
    25: board.D25,
    5: board.D5,
    6: board.D6,
    12: board.D12,
    13: board.D13,
    19: board.D19,
    26: board.D26,
}


class DHT22:
    """Classe pour gérer le capteur DHT22"""
    
    def __init__(self, pin: int = 4):
        """
        Initialise le capteur DHT22
        
        Args:
            pin: Numéro de la broche GPIO (par défaut GPIO 4)
        """
        self.pin = pin
        self.temperature = None
        self.humidity = None
        self.dht = None
        
        try:
            # Convertir le pin GPIO en pin board
            if pin not in PIN_MAPPING:
                raise ValueError(f"Pin GPIO {pin} non supporté. Pins supportés: {list(PIN_MAPPING.keys())}")
            
            board_pin = PIN_MAPPING[pin]
            self.dht = adafruit_dht.DHT22(board_pin, use_pulseio=False)
            logger.info(f"DHT22 initialisé sur GPIO {pin} (board.{board_pin})")
        except Exception as e:
            logger.error(f"Erreur initialisation DHT22: {e}")
            self.dht = None
        
    def read_data(self) -> Optional[Dict]:
        """
        Lit les données du capteur DHT22
        
        Returns:
            Dictionnaire contenant température et humidité ou None en cas d'erreur
        """
        if not self.dht:
            logger.error("DHT22 non initialisé")
            return None
        
        try:
            # La nouvelle bibliothèque peut nécessiter plusieurs tentatives
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    temperature = self.dht.temperature
                    humidity = self.dht.humidity
                    
                    if temperature is not None and humidity is not None:
                        self.temperature = temperature
                        self.humidity = humidity
                        
                        return {
                            'temperature': round(temperature, 2),
                            'humidity': round(humidity, 2),
                            'unit': 'celsius'
                        }
                except RuntimeError as e:
                    # Erreur de lecture, réessayer
                    if attempt < max_retries - 1:
                        time.sleep(0.5)
                        continue
                    else:
                        logger.warning(f"Impossible de lire les données du DHT22 après {max_retries} tentatives: {e}")
                        return None
            
            logger.warning("Impossible de lire les données du DHT22")
            return None
                
        except Exception as e:
            logger.error(f"Erreur lecture DHT22: {e}")
            return None
    
    def get_temperature(self) -> Optional[float]:
        """Retourne la température actuelle"""
        data = self.read_data()
        return data['temperature'] if data else None
    
    def get_humidity(self) -> Optional[float]:
        """Retourne l'humidité actuelle"""
        data = self.read_data()
        return data['humidity'] if data else None







