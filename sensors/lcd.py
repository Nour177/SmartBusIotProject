"""
Module LCD (I2C) pour l'affichage d'informations
Support pour les afficheurs LCD 16x2 ou 20x4 via I2C
"""

import time
from typing import Optional
import logging

logger = logging.getLogger(__name__)

LCD_AVAILABLE = False
LCD_DRIVER_MODE = False

try:
    from RPLCD.i2c import CharLCD
    LCD_AVAILABLE = True
except ImportError:
    try:
        import lcddriver
        LCD_AVAILABLE = True
        LCD_DRIVER_MODE = True
    except ImportError:
        LCD_AVAILABLE = False
        logger.warning("Bibliothèque LCD non disponible. Installation: pip install RPLCD")


class LCD:
    """Classe pour gérer l'afficheur LCD via I2C"""
    
    def __init__(self, i2c_address: int = 0x27, cols: int = 16, rows: int = 2):
        """
        Initialise l'afficheur LCD
        
        Args:
            i2c_address: Adresse I2C du LCD (par défaut 0x27)
            cols: Nombre de colonnes (par défaut 16)
            rows: Nombre de lignes (par défaut 2)
        """
        self.i2c_address = i2c_address
        self.cols = cols
        self.rows = rows
        self.lcd = None
        
        if not LCD_AVAILABLE:
            logger.warning("LCD non disponible - mode simulation")
            return
        
        try:
            if LCD_DRIVER_MODE:
                # Mode avec lcddriver
                self.lcd = lcddriver.lcd()
                logger.info(f"LCD initialisé avec lcddriver - {cols}x{rows}")
            else:
                # Mode avec RPLCD
                self.lcd = CharLCD(
                    i2c_expander='PCF8574',
                    address=i2c_address,
                    cols=cols,
                    rows=rows
                )
                logger.info(f"LCD initialisé - Adresse I2C: {hex(i2c_address)}, {cols}x{rows}")
        except Exception as e:
            logger.error(f"Erreur initialisation LCD: {e}")
            self.lcd = None
    
    def clear(self):
        """Efface l'écran LCD"""
        if self.lcd:
            try:
                self.lcd.clear()
            except Exception as e:
                logger.error(f"Erreur effacement LCD: {e}")
    
    def display(self, line1: str = "", line2: str = "", line3: str = "", line4: str = ""):
        """
        Affiche du texte sur le LCD
        
        Args:
            line1: Texte pour la ligne 1
            line2: Texte pour la ligne 2
            line3: Texte pour la ligne 3 (si 4 lignes)
            line4: Texte pour la ligne 4 (si 4 lignes)
        """
        if not self.lcd:
            logger.debug(f"LCD (simulation):\n{line1}\n{line2}\n{line3}\n{line4}")
            return
        
        try:
            self.clear()
            
            if self.rows >= 1 and line1:
                self.lcd.write_string(line1[:self.cols])
            
            if self.rows >= 2 and line2:
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(line2[:self.cols])
            
            if self.rows >= 3 and line3:
                self.lcd.cursor_pos = (2, 0)
                self.lcd.write_string(line3[:self.cols])
            
            if self.rows >= 4 and line4:
                self.lcd.cursor_pos = (3, 0)
                self.lcd.write_string(line4[:self.cols])
                
        except Exception as e:
            logger.error(f"Erreur affichage LCD: {e}")
    
    def display_door_status(self, entry_distance: Optional[float], exit_distance: Optional[float]):
        """
        Affiche le statut des portes (entrée et sortie)
        
        Args:
            entry_distance: Distance du capteur de la porte d'entrée (cm)
            exit_distance: Distance du capteur de la porte de sortie (cm)
        """
        if not self.lcd:
            logger.info(f"Porte Entrée: {entry_distance} cm | Porte Sortie: {exit_distance} cm")
            return
        
        try:
            # Déterminer l'état des portes
            entry_status = "FERMEE" if entry_distance and entry_distance > 10 else "OUVERTE"
            exit_status = "FERMEE" if exit_distance and exit_distance > 10 else "OUVERTE"
            
            # Ligne 1: Porte d'entrée
            line1 = f"Entree: {entry_status}"
            if entry_distance:
                line1 += f" {entry_distance:.1f}cm"
            
            # Ligne 2: Porte de sortie
            line2 = f"Sortie: {exit_status}"
            if exit_distance:
                line2 += f" {exit_distance:.1f}cm"
            
            self.display(line1, line2)
            
        except Exception as e:
            logger.error(f"Erreur affichage statut portes: {e}")
    
    def display_passenger_count(self, count: int, max_count: int):
        """
        Affiche le nombre de passagers sur le LCD
        
        Args:
            count: Nombre actuel de passagers
            max_count: Nombre maximum de passagers
        """
        if not self.lcd:
            if count >= max_count:
                logger.info(f"BUS PLEIN ({max_count}/{max_count})")
            else:
                logger.info(f"Passagers: {count}/{max_count}")
            return
        
        try:
            # Ligne 1: Nombre de passagers
            if count >= max_count:
                line1 = "BUS PLEIN"
            else:
                line1 = f"Passagers: {count}/{max_count}"
            
            # Ligne 2: Barre de progression ou statut
            if count >= max_count:
                line2 = "Capacite max"
            else:
                # Calculer le pourcentage
                percentage = int((count / max_count) * 100)
                line2 = f"{percentage}% occupe"
            
            self.display(line1, line2)
            
        except Exception as e:
            logger.error(f"Erreur affichage nombre passagers: {e}")
    
    def display_sensor_data(self, data: dict):
        """
        Affiche les données des capteurs sur le LCD
        
        Args:
            data: Dictionnaire contenant les données des capteurs
        """
        if not self.lcd:
            logger.debug(f"Données capteurs (simulation): {data}")
            return
        
        try:
            lines = []
            
            # Température et humidité
            if 'dht22' in data.get('sensors', {}):
                dht = data['sensors']['dht22']
                temp = dht.get('temperature', 'N/A')
                hum = dht.get('humidity', 'N/A')
                lines.append(f"T:{temp}°C H:{hum}%")
            
            # Portes
            entry_dist = None
            exit_dist = None
            if 'ultrasonic_entry' in data.get('sensors', {}):
                entry_dist = data['sensors']['ultrasonic_entry'].get('distance')
            if 'ultrasonic_exit' in data.get('sensors', {}):
                exit_dist = data['sensors']['ultrasonic_exit'].get('distance')
            
            if entry_dist or exit_dist:
                entry_status = "F" if entry_dist and entry_dist > 10 else "O"
                exit_status = "F" if exit_dist and exit_dist > 10 else "O"
                lines.append(f"Portes: E:{entry_status} S:{exit_status}")
            
            # Afficher jusqu'à 4 lignes
            self.display(
                lines[0] if len(lines) > 0 else "",
                lines[1] if len(lines) > 1 else "",
                lines[2] if len(lines) > 2 else "",
                lines[3] if len(lines) > 3 else ""
            )
            
        except Exception as e:
            logger.error(f"Erreur affichage données capteurs: {e}")
    
    def cleanup(self):
        """Nettoie les ressources LCD"""
        if self.lcd:
            try:
                self.clear()
                if hasattr(self.lcd, 'close'):
                    self.lcd.close()
                logger.info("LCD nettoyé")
            except Exception as e:
                logger.error(f"Erreur nettoyage LCD: {e}")

