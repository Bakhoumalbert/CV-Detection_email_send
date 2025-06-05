import mediapipe as mp
import numpy as np
import cv2

class FaceDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect_face_landmarks(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        
        if not results.multi_face_landmarks:
            return None, None

        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = frame.shape
        
        # Points clés pour la détection des lunettes et du chapeau
        nose_tip = face_landmarks.landmark[1]
        left_eye = face_landmarks.landmark[33]
        right_eye = face_landmarks.landmark[263]
        forehead = face_landmarks.landmark[10]

        # Calculer l'inclinaison de la tête
        eye_angle = np.arctan2(right_eye.y - left_eye.y, right_eye.x - left_eye.x)
        head_tilt = np.degrees(eye_angle)

        # Convertir les coordonnées normalisées en pixels
        landmarks_pixels = []
        for landmark in face_landmarks.landmark:
            x, y = int(landmark.x * w), int(landmark.y * h)
            landmarks_pixels.append((x, y))

        return landmarks_pixels, head_tilt

    def detect_accessories(self, frame, landmarks):
        if landmarks is None:
            return False, False

        # Région d'intérêt pour les lunettes (autour des yeux)
        left_eye_region = landmarks[33:46]
        right_eye_region = landmarks[263:276]

        # Région d'intérêt pour le chapeau (au-dessus du front)
        forehead_region = landmarks[10:20]

        # Détection simple basée sur la couleur et la forme
        # À adapter selon vos besoins spécifiques
        has_glasses = self._check_glasses(frame, left_eye_region, right_eye_region)
        has_hat = self._check_hat(frame, forehead_region)

        return has_glasses, has_hat

    def _check_glasses(self, frame, left_eye_region, right_eye_region):
        # Logique de détection des lunettes
        # À implémenter selon vos besoins
        return False

    def _check_hat(self, frame, forehead_region):
        # Logique de détection du chapeau
        # À implémenter selon vos besoins
        return False 