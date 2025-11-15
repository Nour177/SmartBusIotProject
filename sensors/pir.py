"""
Module PIR (Passive Infrared) pour la détection de mouvement
"""

import RPi.GPIO as GPIO
from typing import Optional, Dict
import logging
import time

logger = logging.getLogger(__name__)


class PIR:
    """Classe pour gérer le capteur PIR"""
    
    def __init__(self, pin: int = 18):
        """
        Initialise le capteur PIR
        
        Args:
            pin: Numéro de la broche GPIO (par défaut GPIO 18)
        """
        self.pin = pin
        self.motion_detected = False
        self.last_motion_time = None
        
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            logger.info(f"PIR initialisé sur GPIO {self.pin}")
        except Exception as e:
            logger.error(f"Erreur initialisation PIR: {e}")
    
    def read_data(self) -> Optional[Dict]:
        """
        Lit l'état du capteur PIR
        
        Returns:
            Dictionnaire contenant l'état de détection de mouvement
        """
        try:
            motion = GPIO.input(self.pin)
            self.motion_detected = bool(motion)
            
            if self.motion_detected:
                self.last_motion_time = time.time()
            
            return {
                'motion_detected': self.motion_detected,
                'last_motion_time': self.last_motion_time,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Erreur lecture PIR: {e}")
            return None
    
    def is_motion_detected(self) -> bool:
        """Retourne True si un mouvement est détecté"""
        data = self.read_data()
        return data['motion_detected'] if data else False
    
    def cleanup(self):
        """Nettoie les ressources GPIO"""
        try:
            GPIO.cleanup(self.pin)
            logger.info("PIR nettoyé")
        except Exception as e:
            logger.error(f"Erreur nettoyage PIR: {e}")







