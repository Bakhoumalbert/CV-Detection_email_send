# Système de Détection et Surveillance

Ce projet implémente un système de détection et surveillance utilisant YOLOv8 pour :

1. Détecter les personnes utilisant leur téléphone
2. Détecter les accessoires (chapeau, lunettes) avec prise en compte de l'inclinaison de la tête
3. Envoyer des alertes par email avec les images capturées

## Prérequis

- Python 3.8+
- OpenCV
- Ultralytics YOLOv8
- MediaPipe (pour la détection des points faciaux)
- smtplib (pour l'envoi d'emails)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Modifier le fichier `config.py` avec vos paramètres email :
   - SMTP_SERVER
   - SMTP_PORT
   - EMAIL_SENDER
   - EMAIL_PASSWORD
   - EMAIL_RECEIVER

## Utilisation

```bash
python detection_surveillance.py
```

## Fonctionnalités

### Détection de Téléphone

- Utilise YOLOv8 pour détecter les personnes et les téléphones
- Capture une image lorsqu'une personne utilise son téléphone

### Détection d'Accessoires

- Détecte les chapeaux et lunettes
- Analyse l'inclinaison de la tête pour une meilleure précision
- Utilise MediaPipe pour la détection des points faciaux

### Système d'Alerte

- Envoie automatiquement un email avec l'image capturée
- Inclut un timestamp et les détails de la détection

## Structure du Projet

```
Projet/
├── README.md
├── requirements.txt
├── config.py
├── detection_surveillance.py
└── utils/
    ├── __init__.py
    ├── face_detection.py
    └── email_sender.py
```
