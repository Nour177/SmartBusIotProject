"""
Module pour l'enregistrement des données des capteurs
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class DataLogger:
    """Classe pour enregistrer les données des capteurs"""
    
    def __init__(self, data_dir: str = 'data'):
        """
        Initialise le logger de données
        
        Args:
            data_dir: Répertoire pour stocker les données
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def save_json(self, data: Dict, filename: Optional[str] = None) -> bool:
        """
        Enregistre les données au format JSON
        
        Args:
            data: Données à enregistrer
            filename: Nom du fichier (optionnel, généré automatiquement si non fourni)
        
        Returns:
            True si succès, False sinon
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'sensor_data_{timestamp}.json'
            
            filepath = self.data_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Données sauvegardées: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde JSON: {e}")
            return False
    
    def save_csv(self, data: Dict, filename: str = 'sensor_data.csv') -> bool:
        """
        Enregistre les données au format CSV (append)
        
        Args:
            data: Données à enregistrer
            filename: Nom du fichier CSV
        
        Returns:
            True si succès, False sinon
        """
        try:
            filepath = self.data_dir / filename
            file_exists = filepath.exists()
            
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                # Aplatir les données pour CSV
                flat_data = self._flatten_dict(data)
                
                writer = csv.DictWriter(f, fieldnames=flat_data.keys())
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(flat_data)
            
            logger.debug(f"Données ajoutées au CSV: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde CSV: {e}")
            return False
    
    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Aplatit un dictionnaire imbriqué"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)






