import cv2


class FaceRecognizer:
    _WEIGHTS_PATH = './src/face_recognizer/weights/haarcascade_frontalface_default.xml'
        
    def __init__(self) -> None:
        self._trained_face_data = cv2.CascadeClassifier(self._WEIGHTS_PATH)

    def recognize_faces(self, image):
        face_coordinates = self._get_face_coordinates(image)
        cropped_faces = self._get_crop_faces(image=image, face_coordinates=face_coordinates)
        return (cropped_faces, face_coordinates)

    def _get_face_coordinates(self, image):
        return self._trained_face_data.detectMultiScale(image) 
    
    def _get_crop_faces(self, image, face_coordinates):
        return [image[y:y + h, x:x + w] for (x, y, w, h) in face_coordinates]
