import cv2
import os
from datetime import datetime
from ultralytics import YOLO
from utils.face_detection import FaceDetector
from utils.email_sender import EmailSender
from config import CONFIDENCE_THRESHOLD, HEAD_TILT_THRESHOLD

print("Démarrage du script...")

class SurveillanceSystem:
    def __init__(self):
        print("Initialisation du système de surveillance...")
        # Initialiser YOLO
        print("Chargement du modèle YOLO...")
        self.model = YOLO("yolov8l.pt")
        print("Modèle YOLO chargé avec succès!")
        
        # Initialiser les détecteurs
        print("Initialisation du détecteur facial...")
        self.face_detector = FaceDetector()
        print("Initialisation du système d'email...")
        self.email_sender = EmailSender()
        
        # Créer le dossier pour les captures
        self.capture_dir = "captures"
        os.makedirs(self.capture_dir, exist_ok=True)
        print(f"Dossier de captures créé : {self.capture_dir}")
        
        # Classes d'intérêt
        self.person_class = 0  # ID de la classe "personne"
        self.phone_class = 67  # ID de la classe "téléphone portable"
        print("Initialisation terminée!")

    def process_frame(self, frame):
        # Détection YOLO
        results = self.model(frame, conf=CONFIDENCE_THRESHOLD)
        
        # Détection faciale
        landmarks, head_tilt = self.face_detector.detect_face_landmarks(frame)
        has_glasses, has_hat = self.face_detector.detect_accessories(frame, landmarks)
        
        detection_info = {
            "phone_detected": False,
            "head_tilt": head_tilt if head_tilt is not None else None,
            "has_glasses": has_glasses,
            "has_hat": has_hat
        }

        # Vérifier la détection de téléphone
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if cls == self.person_class:
                    # Vérifier si une personne est détectée
                    person_box = box.xyxy[0].cpu().numpy()
                    
                    # Vérifier si un téléphone est détecté dans la même zone
                    for phone_box in boxes:
                        if int(phone_box.cls[0]) == self.phone_class:
                            phone_coords = phone_box.xyxy[0].cpu().numpy()
                            
                            # Vérifier si le téléphone est proche de la personne
                            if self._check_overlap(person_box, phone_coords):
                                detection_info["phone_detected"] = True
                                
                                # Sauvegarder l'image et envoyer l'alerte
                                self._handle_detection(frame, detection_info)
                                break

        return frame, detection_info

    def _check_overlap(self, box1, box2):
        # Vérifier si deux boîtes se chevauchent
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        
        return x1 < x2 and y1 < y2

    def _handle_detection(self, frame, detection_info):
        # Sauvegarder l'image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(self.capture_dir, f"detection_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        
        # Préparer les informations de détection
        info_text = f"""
        Détection effectuée le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        - Téléphone détecté: {'Oui' if detection_info['phone_detected'] else 'Non'}
        - Inclinaison de la tête: {detection_info['head_tilt']:.2f}° si détectée
        - Lunettes détectées: {'Oui' if detection_info['has_glasses'] else 'Non'}
        - Chapeau détecté: {'Oui' if detection_info['has_hat'] else 'Non'}
        """
        
        # Envoyer l'alerte par email
        self.email_sender.send_alert(image_path, info_text)

def main():
    print("Démarrage de la fonction main...")
    # Initialiser le système
    system = SurveillanceSystem()
    
    # Ouvrir la webcam
    print("Tentative d'ouverture de la webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERREUR: Impossible d'ouvrir la webcam")
        return
    print("Webcam ouverte avec succès!")

    print("Système de surveillance démarré. Appuyez sur 'q' pour quitter.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur de lecture du flux vidéo")
            break

        # Traiter le frame
        processed_frame, detection_info = system.process_frame(frame)
        
        # Afficher les informations sur le frame
        cv2.putText(processed_frame, f"Tilt: {detection_info['head_tilt']:.1f}°" if detection_info['head_tilt'] else "Pas de visage",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Afficher le frame
        cv2.imshow("Surveillance", processed_frame)
        
        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Touche 'q' détectée, arrêt du programme...")
            break

    print("Fermeture de la webcam...")
    cap.release()
    cv2.destroyAllWindows()
    print("Programme terminé.")

if __name__ == "__main__":
    main() 