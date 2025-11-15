"""
Module pour charger la configuration du projet
"""

import json
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Classe pour charger et gérer la configuration"""
    
    def __init__(self, config_file: str = 'config/config.json'):
        """
        Initialise le chargeur de configuration
        
        Args:
            config_file: Chemin vers le fichier de configuration
        """
        self.config_file = Path(config_file)
        self.config = {}
        self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Charge la configuration depuis le fichier JSON
        
        Returns:
            Dictionnaire de configuration
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"Configuration chargée: {self.config_file}")
            else:
                logger.warning(f"Fichier de configuration non trouvé: {self.config_file}")
                self.config = self._get_default_config()
                self.save_config()
        except Exception as e:
            logger.error(f"Erreur chargement configuration: {e}")
            self.config = self._get_default_config()
        
        return self.config
    
    def save_config(self):
        """Sauvegarde la configuration actuelle"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration sauvegardée: {self.config_file}")
        except Exception as e:
            logger.error(f"Erreur sauvegarde configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur de configuration
        
        Args:
            key: Clé de configuration (peut être nested avec '.', ex: 'sensors.gps.port')
            default: Valeur par défaut si la clé n'existe pas
        
        Returns:
            Valeur de configuration ou valeur par défaut
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retourne la configuration par défaut"""
        return {
            "sensors": {
                "gps": {
                    "port": "/dev/ttyAMA0",
                    "baudrate": 9600,
                    "enabled": True
                },
                "dht22": {
                    "pin": 4,
                    "enabled": True
                },
                "mpu9250": {
                    "enabled": True
                },
                "ultrasonic_entry": {
                    "trigger_pin": 23,
                    "echo_pin": 24,
                    "enabled": True,
                    "door_type": "entree"
                },
                "ultrasonic_exit": {
                    "trigger_pin": 25,
                    "echo_pin": 26,
                    "enabled": True,
                    "door_type": "sortie"
                },
                "lcd": {
                    "i2c_address": "0x27",
                    "cols": 16,
                    "rows": 2,
                    "enabled": True
                }
            },
            "bus": {
                "max_passengers": 10,
                "detection_threshold": 3.0
            },
            "data": {
                "save_interval": 5,
                "format": "json",
                "directory": "data"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/smart_bus.log"
            }
        }










