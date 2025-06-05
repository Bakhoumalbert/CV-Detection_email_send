import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from config import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

class EmailSender:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender = EMAIL_SENDER
        self.password = EMAIL_PASSWORD
        self.receiver = EMAIL_RECEIVER

    def send_alert(self, image_path, detection_info):
        if not all([self.sender, self.password, self.receiver]):
            print("Configuration email incomplète. Vérifiez vos variables d'environnement.")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = self.receiver
            msg['Subject'] = f"Alerte de détection - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Corps du message
            body = f"""
            Détection effectuée le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Informations de détection :
            {detection_info}
            """
            msg.attach(MIMEText(body, 'plain'))

            # Attacher l'image
            with open(image_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
                msg.attach(img)

            # Connexion au serveur SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)

            print("Email envoyé avec succès!")
            return True

        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {str(e)}")
            return False 