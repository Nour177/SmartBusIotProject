# Schéma de Circuit Complet - Smart Bus IoT

## Vue d'ensemble
Ce document décrit le schéma de connexion complet pour connecter tous les capteurs du Smart Bus IoT à un Raspberry Pi :
- **2x Capteurs ultrasoniques HC-SR04** (porte d'entrée et porte de sortie)
- **1x Afficheur LCD I2C** (16x2 ou 20x4) pour l'affichage des informations
- **1x Capteur DHT22** (température et humidité)
- **1x MPU9250** (accéléromètre, gyroscope, magnétomètre)
- **1x GPS Neo-6M** (localisation)

## Composants nécessaires
- 1x Raspberry Pi (modèle 3B+, 4, ou compatible)
- 2x Capteurs ultrasoniques HC-SR04 (porte d'entrée et porte de sortie)
- 1x Afficheur LCD I2C 16x2 ou 20x4 (avec module I2C PCF8574)
- 1x Capteur DHT22 (température/humidité)
- 1x Module MPU9250 (9-DOF)
- 1x Module GPS Neo-6M avec antenne
- Résistances de 1kΩ et 2.2kΩ (optionnel, pour protection des HC-SR04)
- Résistance pull-up 4.7kΩ ou 10kΩ (optionnel, pour DHT22)
- Fils de connexion (jumpers)
- Breadboard (recommandé)
- Câble USB (pour GPS si connexion USB)

## Connexions détaillées

### 1. Capteur Ultrasonique - Porte d'Entrée (HC-SR04 #1)
| Broche HC-SR04 | Connexion Raspberry Pi | Description |
|----------------|------------------------|-------------|
| VCC            | 5V (Pin 2)             | Alimentation |
| GND            | GND (Pin 6)            | Masse |
| Trig           | GPIO 23 (Pin 16)       | Signal de déclenchement |
| Echo           | GPIO 24 (Pin 18)       | Signal de réception |

**Note** : Ce capteur détecte l'ouverture/fermeture de la porte d'entrée du bus.

### 2. Capteur Ultrasonique - Porte de Sortie (HC-SR04 #2)
| Broche HC-SR04 | Connexion Raspberry Pi | Description |
|----------------|------------------------|-------------|
| VCC            | 5V (Pin 2)             | Alimentation (partagée) |
| GND            | GND (Pin 6)            | Masse (partagée) |
| Trig           | GPIO 25 (Pin 22)       | Signal de déclenchement |
| Echo           | GPIO 26 (Pin 37)       | Signal de réception |

**Note** : Ce capteur détecte l'ouverture/fermeture de la porte de sortie du bus.

### 3. Afficheur LCD I2C
| Broche LCD Module | Connexion Raspberry Pi | Description |
|-------------------|------------------------|-------------|
| VCC               | 5V (Pin 2)             | Alimentation |
| GND               | GND (Pin 6)            | Masse |
| SDA               | GPIO 2 (Pin 3)         | I2C Data (SDA) - partagé avec MPU9250 |
| SCL               | GPIO 3 (Pin 5)         | I2C Clock (SCL) - partagé avec MPU9250 |

**Note** : 
- L'afficheur LCD utilise le bus I2C (même bus que le MPU9250)
- Adresse I2C par défaut : 0x27 (peut être 0x3F selon le modèle)
- **Fonction principale** : Affiche le nombre de passagers (ex: "Passagers: 5/10" ou "BUS PLEIN")
- Affiche également le pourcentage d'occupation du bus

### 4. Capteur DHT22 (Température/Humidité)
| Broche DHT22 | Connexion Raspberry Pi | Description |
|--------------|------------------------|-------------|
| VCC          | 3.3V (Pin 1) ou 5V (Pin 2) | Alimentation (3.3V recommandé) |
| GND          | GND (Pin 6)            | Masse |
| DATA         | GPIO 4 (Pin 7)         | Données (avec pull-up 4.7kΩ vers VCC) |

### 5. Module MPU9250 (I2C)
| Broche MPU9250 | Connexion Raspberry Pi | Description |
|----------------|------------------------|-------------|
| VCC            | 3.3V (Pin 1)           | Alimentation |
| GND            | GND (Pin 6)            | Masse |
| SDA            | GPIO 2 (Pin 3)         | I2C Data (SDA) |
| SCL            | GPIO 3 (Pin 5)         | I2C Clock (SCL) |

### 6. Module GPS Neo-6M
| Broche GPS Neo-6M | Connexion | Description |
|-------------------|-----------|-------------|
| VCC               | 5V (Pin 2) ou USB | Alimentation |
| GND               | GND (Pin 6) | Masse |
| TX                | USB (via adaptateur USB-Série) | Transmission série |
| RX                | USB (via adaptateur USB-Série) | Réception série |

**Note** : Le GPS Neo-6M se connecte généralement via un adaptateur USB-Série (ex: CP2102, CH340) sur le port USB du Raspberry Pi (`/dev/ttyUSB0`).

## Schéma de connexion complet (ASCII)

```
                    Raspberry Pi
    ┌─────────────────────────────────────────────────┐
    │                                                 │
    │  Pin 1  (3.3V) ──────┬─────────────────────────┤
    │                      │                         │
    │  Pin 2  (5V)  ───────┼─────────────────────────┤
    │                      │                         │
    │  Pin 3  (GPIO 2/SDA) ┼─────────────────────────┤
    │                      │                         │
    │  Pin 5  (GPIO 3/SCL) ┼─────────────────────────┤
    │                      │                         │
    │  Pin 6  (GND) ───────┼─────────────────────────┤
    │                      │                         │
    │  Pin 7  (GPIO 4) ─────┼─────────────────────────┤
    │                      │                         │
    │  Pin 16 (GPIO 23) ────┼─────────────────────────┤
    │                      │                         │
    │  Pin 18 (GPIO 24) ────┼─────────────────────────┤
    │                      │                         │
    │  Pin 22 (GPIO 25) ────┼─────────────────────────┤
    │                      │                         │
    │  Pin 37 (GPIO 26) ────┼─────────────────────────┤
    │                                                 │
    │  USB Port ─────────────────────────────────────┤
    └─────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┬──────────────┐
        │                 │                 │              │
   ┌────▼────┐      ┌─────▼─────┐    ┌─────▼─────┐  ┌─────▼─────┐
   │ HC-SR04 │      │   DHT22   │    │  MPU9250  │  │ GPS Neo-6M│
   │   #1    │      │           │    │           │  │           │
   │         │      │ VCC ──────┼────┼─── VCC    │  │ VCC ──────┼─── USB
   │ VCC ────┼──────┼─── VCC    │    │           │  │           │
   │ GND ────┼──────┼─── GND    │    │ GND ──────┼──┼─── GND    │
   │ Trig ───┼── GPIO 23        │    │           │  │           │
   │ Echo ───┼── GPIO 24        │    │ DATA ─────┼──┼─── GPIO 4 │
   │         │      │           │    │           │  │           │
   └─────────┘      └───────────┘    │ SDA ──────┼──┼─── GPIO 2 │
                                      │ SCL ──────┼──┼─── GPIO 3 │
   ┌────▼────┐                        └───────────┘  └───────────┘
   │ HC-SR04 │
   │   #2    │
   │         │
   │ VCC ────┼─── (partagé avec HC-SR04 #1)
   │ GND ────┼─── (partagé)
   │ Trig ───┼─── GPIO 25
   │ Echo ───┼─── GPIO 26
   └─────────┘
```

## Schéma détaillé des broches Raspberry Pi

```
Raspberry Pi GPIO Header (40 pins)

    3.3V  [1]  [2]  5V        ← DHT22 VCC, MPU9250 VCC, HC-SR04 VCC, GPS VCC
   GPIO2  [3]  [4]  5V        ← MPU9250 SDA (I2C)
   GPIO3  [5]  [6]  GND       ← MPU9250 SCL (I2C), Masse commune
   GPIO4  [7]  [8]  GPIO14    ← DHT22 DATA
     GND  [9]  [10] GPIO15
  GPIO17 [11]  [12] GPIO18
  GPIO27 [13]  [14] GND
  GPIO22 [15]  [16] GPIO23    ← HC-SR04 #1 Trig
    3.3V [17]  [18] GPIO24    ← HC-SR04 #1 Echo
  GPIO10 [19]  [20] GND
   GPIO9 [21]  [22] GPIO25    ← HC-SR04 #2 Trig
  GPIO11 [23]  [24] GPIO8
     GND [25]  [26] GPIO7
   GPIO0 [27]  [28] GPIO1
   GPIO5 [29]  [30] GND
   GPIO6 [31]  [32] GPIO12
  GPIO13 [33]  [34] GND
  GPIO19 [35]  [36] GPIO16
  GPIO26 [37]  [38] GPIO20    ← HC-SR04 #2 Echo
     GND [39]  [40] GPIO21
```

## Tableau récapitulatif des GPIO utilisés

| GPIO | Broche Physique | Capteur | Fonction |
|------|----------------|---------|----------|
| GPIO 2 | Pin 3 | MPU9250 | I2C SDA |
| GPIO 3 | Pin 5 | MPU9250 | I2C SCL |
| GPIO 4 | Pin 7 | DHT22 | Data |
| GPIO 23 | Pin 16 | HC-SR04 #1 | Trigger |
| GPIO 24 | Pin 18 | HC-SR04 #1 | Echo |
| GPIO 25 | Pin 22 | HC-SR04 #2 | Trigger |
| GPIO 26 | Pin 37 | HC-SR04 #2 | Echo |

## Alimentation

### Répartition de l'alimentation
- **3.3V (Pin 1)** : DHT22, MPU9250
- **5V (Pin 2)** : HC-SR04 #1, HC-SR04 #2, GPS Neo-6M (si connecté directement)
- **GND (Pin 6)** : Masse commune pour tous les capteurs

### Consommation estimée
- HC-SR04 : ~15mA chacun (30mA total)
- DHT22 : ~1-2mA
- MPU9250 : ~3-4mA
- GPS Neo-6M : ~20-30mA
- **Total estimé** : ~55-65mA (bien en dessous de la limite du Raspberry Pi)

## Protection et résistances

### Protection des HC-SR04 (optionnel mais recommandé)
Les broches Echo des HC-SR04 délivrent 5V, mais les GPIO du Raspberry Pi acceptent maximum 3.3V. Pour protéger les GPIO :

**Diviseur de tension sur chaque broche Echo :**
- Résistance de 1kΩ entre Echo du HC-SR04 et GPIO
- Résistance de 2.2kΩ entre GPIO et GND
- Cela réduit la tension de 5V à ~3.3V

### Pull-up pour DHT22
Le DHT22 nécessite une résistance pull-up de 4.7kΩ à 10kΩ entre la broche DATA et VCC. Certains modules DHT22 l'intègrent déjà.

## Configuration I2C pour MPU9250

Avant d'utiliser le MPU9250, activez l'interface I2C sur le Raspberry Pi :

```bash
sudo raspi-config
# Interface Options → I2C → Enable
```

Vérifiez la détection du module :
```bash
sudo i2cdetect -y 1
```

L'adresse I2C du MPU9250 est généralement `0x68` ou `0x69`.

## Configuration GPS

Le GPS Neo-6M se connecte via USB. Vérifiez le port série :

```bash
ls -l /dev/ttyUSB*
# ou
ls -l /dev/ttyACM*
```

Configurez les permissions si nécessaire :
```bash
sudo usermod -a -G dialout $USER
```

## Configuration dans config.json

Exemple de configuration complète :

```json
{
  "sensors": {
    "gps": {
      "port": "/dev/ttyUSB0",
      "baudrate": 9600,
      "enabled": true
    },
    "dht22": {
      "pin": 4,
      "enabled": true
    },
    "mpu9250": {
      "enabled": true
    },
    "ultrasonic_entry": {
      "trigger_pin": 23,
      "echo_pin": 24,
      "enabled": true,
      "door_type": "entree"
    },
    "ultrasonic_exit": {
      "trigger_pin": 25,
      "echo_pin": 26,
      "enabled": true,
      "door_type": "sortie"
    },
    "lcd": {
      "i2c_address": "0x27",
      "cols": 16,
      "rows": 2,
      "enabled": true
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
```

## Système de comptage de passagers

Le système utilise les capteurs ultrason pour compter automatiquement les passagers :

- **Détection** : Un passager est détecté lorsque la distance mesurée est ≤ 3cm (configurable via `bus.detection_threshold`)
- **Porte d'entrée** : Incrémente le compteur de passagers
- **Porte de sortie** : Décrémente le compteur de passagers
- **Maximum** : 10 passagers par défaut (configurable via `bus.max_passengers`)
- **Affichage LCD** : 
  - Affiche "Passagers: X/10" quand il y a de la place
  - Affiche "BUS PLEIN" quand la capacité maximale est atteinte
  - Affiche le pourcentage d'occupation sur la deuxième ligne

## Ordre de montage recommandé

1. **Alimentation et masse** : Connectez d'abord toutes les masses (GND) et alimentations
2. **I2C (MPU9250)** : Connectez le MPU9250 (SDA/SCL)
3. **GPIO simples** : Connectez le DHT22
4. **Ultrasoniques** : Connectez les deux HC-SR04
5. **GPS** : Connectez le GPS via USB en dernier

## Vérification du circuit

### Tests individuels

1. **DHT22** : Testez la lecture de température/humidité
2. **MPU9250** : Vérifiez la détection I2C avec `i2cdetect`
3. **HC-SR04 #1** : Testez la mesure de distance
4. **HC-SR04 #2** : Testez la mesure de distance
5. **GPS** : Vérifiez la réception de données NMEA

### Tests de compatibilité

- Vérifiez qu'il n'y a pas de conflits de GPIO
- Testez tous les capteurs simultanément
- Vérifiez la stabilité de l'alimentation

## Dépannage

### Problèmes courants

**HC-SR04 - Pas de lecture :**
- Vérifiez les connexions VCC et GND
- Vérifiez que les broches Trig et Echo sont correctes
- Ajoutez les résistances de protection si nécessaire

**DHT22 - Erreurs de lecture :**
- Vérifiez la résistance pull-up (4.7kΩ-10kΩ)
- Vérifiez que le GPIO 4 est correctement configuré
- Le DHT22 peut nécessiter un délai entre les lectures

**MPU9250 - Non détecté :**
- Activez l'interface I2C : `sudo raspi-config`
- Vérifiez les connexions SDA/SCL
- Vérifiez l'alimentation 3.3V
- Utilisez `i2cdetect -y 1` pour vérifier la détection

**GPS - Pas de données :**
- Vérifiez le port série : `ls -l /dev/ttyUSB*`
- Vérifiez les permissions : `sudo usermod -a -G dialout $USER`
- Le GPS nécessite une vue dégagée du ciel pour fonctionner
- Attendez quelques minutes pour la première acquisition de signal

**Interférences entre capteurs :**
- Évitez de déclencher les deux HC-SR04 simultanément
- Utilisez des délais entre les mesures
- Placez les capteurs à une distance suffisante

## Notes de sécurité

- ⚠️ **Ne connectez jamais directement 5V sur les GPIO** (sauf avec protection)
- ⚠️ **Vérifiez toutes les connexions avant d'alimenter le Raspberry Pi**
- ⚠️ **Utilisez des résistances de protection pour les broches Echo des HC-SR04**
- ⚠️ **Respectez la polarité des alimentations (VCC/GND)**

## Schéma de câblage sur breadboard (vue de dessus)

```
Breadboard Layout (vue simplifiée)

    + Rail 5V ──────────────────────────────── (Pin 2)
    - Rail GND ──────────────────────────────── (Pin 6)
    
    [HC-SR04 #1]    [HC-SR04 #2]    [DHT22]    [MPU9250]
    VCC → 5V Rail   VCC → 5V Rail   VCC → 3.3V  VCC → 3.3V
    GND → GND Rail  GND → GND Rail  GND → GND   GND → GND
    Trig → GPIO 23  Trig → GPIO 25  DATA → GPIO4 SDA → GPIO2
    Echo → GPIO 24  Echo → GPIO 26              SCL → GPIO3
```

---

**Document créé pour le projet Smart Bus IoT - ProjetPI4**
