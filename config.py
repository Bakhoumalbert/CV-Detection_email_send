import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "")

# Configuration de la détection
CONFIDENCE_THRESHOLD = 0.5
HEAD_TILT_THRESHOLD = 20  # degrés 