"""
Module Ultrasonic (HC-SR04) pour la mesure de distance
"""

import RPi.GPIO as GPIO
import time
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class Ultrasonic:
    """Classe pour gérer le capteur ultrasonique HC-SR04"""
    
    def __init__(self, trigger_pin: int = 23, echo_pin: int = 24):
        """
        Initialise le capteur ultrasonique
        
        Args:
            trigger_pin: Broche GPIO pour le trigger (par défaut GPIO 23)
            echo_pin: Broche GPIO pour l'echo (par défaut GPIO 24)
        """
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.distance = None
        
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.trigger_pin, GPIO.OUT)
            GPIO.setup(self.echo_pin, GPIO.IN)
            logger.info(f"Ultrasonic initialisé - Trigger: GPIO {trigger_pin}, Echo: GPIO {echo_pin}")
        except Exception as e:
            logger.error(f"Erreur initialisation Ultrasonic: {e}")
    
    def read_data(self) -> Optional[Dict]:
        """
        Lit la distance mesurée par le capteur
        
        Returns:
            Dictionnaire contenant la distance en cm
        """
        try:
            # Envoi d'une impulsion
            GPIO.output(self.trigger_pin, False)
            time.sleep(0.000002)
            GPIO.output(self.trigger_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, False)
            
            # Attente de la réponse - Attendre que echo passe à HIGH
            timeout_start = time.time()
            pulse_start = None
            
            # Attendre que l'echo passe à HIGH (début du signal)
            while GPIO.input(self.echo_pin) == 0:
                if time.time() - timeout_start > 0.1:  # Timeout après 100ms
                    logger.warning(f"Ultrasonic timeout - Echo n'a pas démarré (GPIO {self.echo_pin})")
                    return None
            pulse_start = time.time()
            
            # Attendre que l'echo repasse à LOW (fin du signal)
            timeout_start = time.time()
            while GPIO.input(self.echo_pin) == 1:
                pulse_end = time.time()
                if time.time() - timeout_start > 0.1:  # Timeout après 100ms
                    logger.warning(f"Ultrasonic timeout - Echo n'a pas fini (GPIO {self.echo_pin})")
                    return None
            
            # Calcul de la distance
            if pulse_start is None:
                return None
                
            pulse_duration = pulse_end - pulse_start
            distance = (pulse_duration * 34300) / 2  # Vitesse du son = 343 m/s
            
            # Limitation de la plage de mesure (2-400 cm)
            if distance < 2 or distance > 400:
                logger.debug(f"Ultrasonic distance hors plage: {distance} cm (GPIO {self.echo_pin})")
                return None
            
            self.distance = round(distance, 2)
            
            return {
                'distance': self.distance,
                'unit': 'cm',
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Erreur lecture Ultrasonic (GPIO {self.echo_pin}): {e}")
            return None
    
    def get_distance(self) -> Optional[float]:
        """Retourne la distance mesurée"""
        data = self.read_data()
        return data['distance'] if data else None
    
    def cleanup(self):
        """Nettoie les ressources GPIO"""
        try:
            GPIO.cleanup([self.trigger_pin, self.echo_pin])
            logger.info("Ultrasonic nettoyé")
        except Exception as e:
            logger.error(f"Erreur nettoyage Ultrasonic: {e}")




















