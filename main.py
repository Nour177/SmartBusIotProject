"""
Programme principal du Smart Bus IoT
Rassemble les données de tous les capteurs et les enregistre
"""

import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from sensors import GPSNeo6M, DHT22, MPU9250, Ultrasonic, LCD
from utils import DataLogger, ConfigLoader, HTTPClient

# Configuration du logging
Path('logs').mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/smart_bus.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class SmartBus:
    """Classe principale pour gérer le Smart Bus"""
    
    def __init__(self, config_file: str = 'config/config.json'):
        """
        Initialise le Smart Bus avec tous les capteurs
        
        Args:
            config_file: Chemin vers le fichier de configuration
        """
        self.config = ConfigLoader(config_file)
        self.data_logger = DataLogger(
            self.config.get('data.directory', 'data')
        )
        
        # Initialisation du client HTTP pour envoyer les données au serveur FastAPI
        self.http_client = None
        if self.config.get('server.enabled', False):
            server_url = self.config.get('server.url', 'http://192.168.1.100:8000')
            timeout = self.config.get('server.timeout', 5)
            retry_count = self.config.get('server.retry_count', 3)
            self.http_client = HTTPClient(server_url, timeout=timeout, retry_count=retry_count)
            
            # Test de connexion au démarrage
            if self.http_client.test_connection():
                logger.info("✅ Connexion au serveur FastAPI réussie")
            else:
                logger.warning("⚠️ Impossible de se connecter au serveur FastAPI - Les données seront uniquement sauvegardées localement")
        
        # Initialisation des capteurs
        self.sensors = {}
        
        if self.config.get('sensors.gps.enabled', True):
            self.sensors['gps'] = GPSNeo6M(
                port=self.config.get('sensors.gps.port', '/dev/serial0'),
                baudrate=self.config.get('sensors.gps.baudrate', 9600)
            )
            self.sensors['gps'].connect()
        
        if self.config.get('sensors.dht22.enabled', True):
            self.sensors['dht22'] = DHT22(
                pin=self.config.get('sensors.dht22.pin', 4)
            )
        
        if self.config.get('sensors.mpu9250.enabled', True):
            self.sensors['mpu9250'] = MPU9250()
        
        # Capteur ultrason pour la porte d'entrée
        if self.config.get('sensors.ultrasonic_entry.enabled', True):
            self.sensors['ultrasonic_entry'] = Ultrasonic(
                trigger_pin=self.config.get('sensors.ultrasonic_entry.trigger_pin', 23),
                echo_pin=self.config.get('sensors.ultrasonic_entry.echo_pin', 24)
            )
        
        # Capteur ultrason pour la porte de sortie
        if self.config.get('sensors.ultrasonic_exit.enabled', True):
            self.sensors['ultrasonic_exit'] = Ultrasonic(
                trigger_pin=self.config.get('sensors.ultrasonic_exit.trigger_pin', 25),
                echo_pin=self.config.get('sensors.ultrasonic_exit.echo_pin', 26)
            )
        
        # Afficheur LCD
        if self.config.get('sensors.lcd.enabled', True):
            i2c_addr = self.config.get('sensors.lcd.i2c_address', '0x27')
            # Convertir l'adresse hexadécimale en entier
            if isinstance(i2c_addr, str):
                i2c_addr = int(i2c_addr, 16)
            self.lcd = LCD(
                i2c_address=i2c_addr,
                cols=self.config.get('sensors.lcd.cols', 16),
                rows=self.config.get('sensors.lcd.rows', 2)
            )
        else:
            self.lcd = None
        
        # Compteur de passagers
        self.passenger_count = 0
        self.max_passengers = self.config.get('bus.max_passengers', 10)
        self.detection_threshold = self.config.get('bus.detection_threshold', 3.0)  # 3cm
        self.entry_detected = False  # Évite les détections multiples
        self.exit_detected = False
        
        logger.info(f"Smart Bus initialisé avec {len(self.sensors)} capteur(s)")
        logger.info(f"Capacité maximale: {self.max_passengers} passagers")
    
    def collect_data(self) -> dict:
        """
        Collecte les données de tous les capteurs
        
        Returns:
            Dictionnaire contenant toutes les données des capteurs
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'sensors': {}
        }
        
        # Collecte des données GPS
        if 'gps' in self.sensors:
            gps_data = self.sensors['gps'].read_data()
            # Toujours inclure les données GPS même sans fix pour voir le statut
            if gps_data:
                data['sensors']['gps'] = gps_data
        
        # Collecte des données DHT22
        if 'dht22' in self.sensors:
            dht22_data = self.sensors['dht22'].read_data()
            if dht22_data:
                data['sensors']['dht22'] = dht22_data
        
        # Collecte des données MPU9250
        if 'mpu9250' in self.sensors:
            mpu_data = self.sensors['mpu9250'].read_data()
            if mpu_data:
                data['sensors']['mpu9250'] = mpu_data
        
        # Collecte des données Ultrasonic - Porte d'entrée
        entry_distance = None
        if 'ultrasonic_entry' in self.sensors:
            ultrasonic_entry_data = self.sensors['ultrasonic_entry'].read_data()
            if ultrasonic_entry_data:
                ultrasonic_entry_data['door_type'] = 'entree'
                entry_distance = ultrasonic_entry_data.get('distance')
                data['sensors']['ultrasonic_entry'] = ultrasonic_entry_data
        
        # Collecte des données Ultrasonic - Porte de sortie
        exit_distance = None
        if 'ultrasonic_exit' in self.sensors:
            ultrasonic_exit_data = self.sensors['ultrasonic_exit'].read_data()
            if ultrasonic_exit_data:
                ultrasonic_exit_data['door_type'] = 'sortie'
                exit_distance = ultrasonic_exit_data.get('distance')
                data['sensors']['ultrasonic_exit'] = ultrasonic_exit_data
        
        # Détection et comptage des passagers
        self._detect_passengers(entry_distance, exit_distance)
        
        # Ajouter le nombre de passagers aux données
        data['passengers'] = {
            'count': self.passenger_count,
            'max': self.max_passengers,
            'is_full': self.passenger_count >= self.max_passengers
        }
        
        # Ajouter bus_id si configuré
        bus_id = self.config.get('server.bus_id', 'Bus1')
        data['bus_id'] = bus_id
        
        # Affichage sur LCD si disponible
        if self.lcd:
            self.lcd.display_passenger_count(self.passenger_count, self.max_passengers)
        
        return data
    
    def _detect_passengers(self, entry_distance: Optional[float], exit_distance: Optional[float]):
        """
        Détecte les passagers aux portes et met à jour le compteur
        
        Args:
            entry_distance: Distance mesurée à la porte d'entrée (cm)
            exit_distance: Distance mesurée à la porte de sortie (cm)
        """
        # Détection à la porte d'entrée (passager entre)
        if entry_distance is not None and entry_distance <= self.detection_threshold:
            if not self.entry_detected:
                # Nouveau passager détecté
                if self.passenger_count < self.max_passengers:
                    self.passenger_count += 1
                    logger.info(f"Passager entré! Total: {self.passenger_count}/{self.max_passengers}")
                else:
                    logger.warning(f"Bus plein! Impossible d'ajouter un passager")
                self.entry_detected = True
        else:
            # Plus de passager détecté, réinitialiser le flag
            self.entry_detected = False
        
        # Détection à la porte de sortie (passager sort)
        if exit_distance is not None and exit_distance <= self.detection_threshold:
            if not self.exit_detected:
                # Passager sorti
                if self.passenger_count > 0:
                    self.passenger_count -= 1
                    logger.info(f"Passager sorti! Total: {self.passenger_count}/{self.max_passengers}")
                else:
                    logger.warning(f"Bus vide! Impossible de retirer un passager")
                self.exit_detected = True
        else:
            # Plus de passager détecté, réinitialiser le flag
            self.exit_detected = False
    
    def run(self, interval: int = 5):
        """
        Lance la boucle principale de collecte de données
        
        Args:
            interval: Intervalle entre les collectes en secondes
        """
        logger.info(f"Démarrage de la collecte de données (intervalle: {interval}s)")
        
        try:
            while True:
                # Collecte des données
                data = self.collect_data()
                
                # Affichage des capteurs actifs
                active_sensors = data['sensors'].keys()
                if active_sensors:
                    sensors_str = ', '.join(sorted(active_sensors))
                else:
                    sensors_str = 'aucun capteur actif'
                logger.info(f"Capteurs actifs: {sensors_str}")
                
                # Sauvegarde locale des données
                save_format = self.config.get('data.format', 'json')
                if save_format == 'json':
                    self.data_logger.save_json(data)
                elif save_format == 'csv':
                    self.data_logger.save_csv(data)
                else:
                    self.data_logger.save_json(data)
                    self.data_logger.save_csv(data)
                
                # Envoi des données au serveur FastAPI si activé
                if self.http_client:
                    if self.http_client.send_data(data):
                        logger.info("✅ Données envoyées au serveur FastAPI")
                    else:
                        logger.warning("⚠️ Échec de l'envoi des données au serveur")
                else:
                    logger.warning("⚠️ HTTP Client non initialisé - Les données ne sont pas envoyées au serveur")
                
                # Attente avant la prochaine collecte
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Arrêt demandé par l'utilisateur")
        except Exception as e:
            logger.error(f"Erreur dans la boucle principale: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Nettoie les ressources et ferme les connexions"""
        logger.info("Nettoyage des ressources...")
        
        if 'gps' in self.sensors:
            self.sensors['gps'].disconnect()
        
        if 'ultrasonic_entry' in self.sensors:
            self.sensors['ultrasonic_entry'].cleanup()
        
        if 'ultrasonic_exit' in self.sensors:
            self.sensors['ultrasonic_exit'].cleanup()
        
        if self.lcd:
            self.lcd.cleanup()
        
        logger.info("Nettoyage terminé")


def main():
    """Point d'entrée principal"""
    try:
        smart_bus = SmartBus()
        interval = smart_bus.config.get('data.save_interval', 5)
        smart_bus.run(interval=interval)
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        raise


if __name__ == '__main__':
    main()





