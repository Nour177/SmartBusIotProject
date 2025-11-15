"""
Module DHT22 pour la mesure de température et d'humidité
"""

import Adafruit_DHT
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class DHT22:
    """Classe pour gérer le capteur DHT22"""
    
    SENSOR_TYPE = Adafruit_DHT.DHT22
    
    def __init__(self, pin: int = 4):
        """
        Initialise le capteur DHT22
        
        Args:
            pin: Numéro de la broche GPIO (par défaut GPIO 4)
        """
        self.pin = pin
        self.temperature = None
        self.humidity = None
        
    def read_data(self) -> Optional[Dict]:
        """
        Lit les données du capteur DHT22
        
        Returns:
            Dictionnaire contenant température et humidité ou None en cas d'erreur
        """
        try:
            humidity, temperature = Adafruit_DHT.read_retry(
                self.SENSOR_TYPE,
                self.pin
            )
            
            if humidity is not None and temperature is not None:
                self.temperature = temperature
                self.humidity = humidity
                
                return {
                    'temperature': round(temperature, 2),
                    'humidity': round(humidity, 2),
                    'unit': 'celsius'
                }
            else:
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






