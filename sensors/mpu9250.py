"""
Module MPU9250 pour la mesure d'accélération, gyroscope et magnétomètre
"""

import time
from typing import Optional, Dict
import logging

try:
    from mpu9250_jmdev import registers
    try:
        from mpu9250_jmdev.mpu_9250 import MPU9250 as _MPU9250_CLASS
    except ImportError:
        # Certains environnements exposent la classe via un sous-module
        import mpu9250_jmdev.mpu_9250 as _mpu_module  # type: ignore
        _MPU9250_CLASS = getattr(_mpu_module, "MPU9250", None)
    MPU9250_AVAILABLE = _MPU9250_CLASS is not None
except ImportError:
    _MPU9250_CLASS = None
    registers = None
    MPU9250_AVAILABLE = False
    logging.warning("mpu9250_jmdev non disponible, utilisation d'un mock")

logger = logging.getLogger(__name__)


class MPU9250:
    """Classe pour gérer le capteur MPU9250"""
    
    def __init__(self):
        """Initialise le capteur MPU9250"""
        self.mpu = None
        self.acceleration = None
        self.gyroscope = None
        self.magnetometer = None
        
        if MPU9250_AVAILABLE and callable(_MPU9250_CLASS):
            try:
                # Vérifier les attributs disponibles dans registers
                mfs_value = None
                if hasattr(registers, 'MFS_14BITS'):
                    mfs_value = registers.MFS_14BITS
                elif hasattr(registers, 'MFS_16BITS'):
                    mfs_value = registers.MFS_16BITS
                else:
                    # Valeur par défaut pour 14 bits (0x00)
                    mfs_value = 0x00
                    logger.debug("Utilisation de la valeur par défaut pour mfs (0x00)")
                
                # Configuration du MPU9250
                init_params = {
                    'address_ak': registers.AK8963_ADDRESS,
                    'address_mpu_master': registers.MPU9050_ADDRESS_68,
                    'bus': 1,
                    'gfs': registers.AFS_2G,
                    'afs': registers.AFS_2G,
                    'mode': registers.AK8963_MODE_C100HZ
                }
                
                # Ajouter mfs seulement si disponible ou utiliser la valeur par défaut
                init_params['mfs'] = mfs_value
                
                self.mpu = _MPU9250_CLASS(**init_params)
                self.mpu.configure()
                logger.info("MPU9250 initialisé")
            except TypeError:
                logger.error(
                    "La classe MPU9250 n'a pas été trouvée dans mpu9250_jmdev. "
                    "Vérifiez l'installation de la bibliothèque."
                )
                self.mpu = None
            except Exception as e:
                logger.error(f"Erreur initialisation MPU9250: {e}")
                self.mpu = None
        else:
            logger.warning("MPU9250 en mode mock (bibliothèque non disponible)")
    
    def read_data(self) -> Optional[Dict]:
        """
        Lit les données du capteur MPU9250
        
        Returns:
            Dictionnaire contenant accélération, gyroscope et magnétomètre
        """
        if not MPU9250_AVAILABLE or not self.mpu:
            # Mode mock pour développement
            return {
                'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0},
                'gyroscope': {'x': 0.0, 'y': 0.0, 'z': 0.0},
                'magnetometer': {'x': 0.0, 'y': 0.0, 'z': 0.0}
            }
        
        try:
            # Lecture des données
            accel = self.mpu.readAccelerometerMaster()
            gyro = self.mpu.readGyroscopeMaster()
            mag = self.mpu.readMagnetometerMaster()
            
            self.acceleration = {
                'x': round(accel[0], 3),
                'y': round(accel[1], 3),
                'z': round(accel[2], 3)
            }
            
            self.gyroscope = {
                'x': round(gyro[0], 3),
                'y': round(gyro[1], 3),
                'z': round(gyro[2], 3)
            }
            
            self.magnetometer = {
                'x': round(mag[0], 3),
                'y': round(mag[1], 3),
                'z': round(mag[2], 3)
            }
            
            return {
                'acceleration': self.acceleration,
                'gyroscope': self.gyroscope,
                'magnetometer': self.magnetometer
            }
            
        except Exception as e:
            logger.error(f"Erreur lecture MPU9250: {e}")
            return None
    
    def get_acceleration(self) -> Optional[Dict]:
        """Retourne les valeurs d'accélération"""
        data = self.read_data()
        return data['acceleration'] if data else None
    
    def get_gyroscope(self) -> Optional[Dict]:
        """Retourne les valeurs du gyroscope"""
        data = self.read_data()
        return data['gyroscope'] if data else None
    
    def get_magnetometer(self) -> Optional[Dict]:
        """Retourne les valeurs du magnétomètre"""
        data = self.read_data()
        return data['magnetometer'] if data else None




