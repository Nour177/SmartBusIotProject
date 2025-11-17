"""
Module pour envoyer les données au serveur FastAPI via HTTP POST
"""

import requests
import logging
from typing import Dict, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class HTTPClient:
    """Classe pour envoyer les données au serveur FastAPI"""
    
    def __init__(self, server_url: str, timeout: int = 5, retry_count: int = 3):
        """
        Initialise le client HTTP
        
        Args:
            server_url: URL du serveur FastAPI (ex: http://192.168.1.100:8000)
            timeout: Timeout en secondes pour les requêtes
            retry_count: Nombre de tentatives en cas d'échec
        """
        # S'assurer que l'URL ne se termine pas par /
        if server_url.endswith('/'):
            server_url = server_url.rstrip('/')
        
        self.server_url = server_url
        self.timeout = timeout
        self.retry_count = retry_count
        self.endpoint = f"{server_url}/api/data"
        self.health_endpoint = f"{server_url}/api/health"
        
        logger.info(f"HTTP Client initialisé - Serveur: {self.server_url}")
    
    def send_data(self, data: Dict) -> bool:
        """
        Envoie les données au serveur FastAPI via HTTP POST
        
        Args:
            data: Dictionnaire contenant les données des capteurs
        
        Returns:
            True si succès, False sinon
        """
        # Ajouter un bus_id si non présent
        if 'bus_id' not in data:
            data['bus_id'] = 'Bus1'  # Par défaut
        
        # S'assurer que le timestamp est présent
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        for attempt in range(self.retry_count):
            try:
                response = requests.post(
                    self.endpoint,
                    json=data,
                    headers={'Content-Type': 'application/json'},
                    timeout=self.timeout
                )
                
                if response.status_code == 200 or response.status_code == 201:
                    logger.debug(f"Données envoyées avec succès: {response.status_code}")
                    return True
                else:
                    logger.warning(
                        f"Erreur serveur (tentative {attempt + 1}/{self.retry_count}): "
                        f"{response.status_code} - {response.text}"
                    )
                    
            except requests.exceptions.Timeout:
                logger.warning(
                    f"Timeout (tentative {attempt + 1}/{self.retry_count}): "
                    f"Le serveur n'a pas répondu dans les {self.timeout}s"
                )
            except requests.exceptions.ConnectionError:
                logger.warning(
                    f"Erreur de connexion (tentative {attempt + 1}/{self.retry_count}): "
                    f"Impossible de se connecter au serveur {self.server_url}"
                )
            except Exception as e:
                logger.error(f"Erreur inattendue lors de l'envoi: {e}")
            
            # Attendre avant de réessayer (sauf pour la dernière tentative)
            if attempt < self.retry_count - 1:
                import time
                time.sleep(1)
        
        logger.error(f"Échec de l'envoi après {self.retry_count} tentatives")
        return False
    
    def test_connection(self) -> bool:
        """
        Teste la connexion au serveur FastAPI
        
        Returns:
            True si le serveur répond, False sinon
        """
        try:
            response = requests.get(self.health_endpoint, timeout=self.timeout)
            if response.status_code == 200:
                logger.info("Connexion au serveur FastAPI réussie")
                return True
            else:
                logger.warning(f"Le serveur répond mais avec un code d'erreur: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            logger.warning(f"Impossible de se connecter au serveur {self.server_url}")
            return False
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout lors de la connexion au serveur {self.server_url}")
            return False
        except Exception as e:
            logger.error(f"Erreur lors du test de connexion: {e}")
            return False

