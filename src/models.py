import numpy as np
import cv2

from src.face_recognizer.recognizer import FaceRecognizer
from src.emotion_classificator.classificator import EmotionClassificator
from src.utils import process_image, registrate_user


class ApiModel:
    face_recognizer = FaceRecognizer()
    emotion_classificator = EmotionClassificator()
    
    def registrate_emotions(self, content):
        nparr = np.frombuffer(content, np.uint8)
        image = cv2.imdecode(nparr, 1)
    
        faces, coordinates = self.face_recognizer.recognize_faces(image=image)
        emotions = self.emotion_classificator.classify_emotions(data=faces)
        
        result = [] # return
        for t, l in zip(coordinates, emotions):
            coords = {} # x, y, width, height
            box_and_labels = {} # box, label
            coords['x'], coords['y'], coords['width'], coords['height'] = int(t[0]), int(t[1]), int(t[2]), int(t[3])
            box_and_labels["box"], box_and_labels["label"] = coords, l 
            result.append(box_and_labels)
            
        return result
