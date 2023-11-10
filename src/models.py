import numpy as np
import cv2

from src.face_recognizer.recognizer import FaceRecognizer
from src.emotion_classificator.classificator import EmotionClassificator
from src.utils import process_image, registrate_user
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

EMOTIONS = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']


class ApiModel:
    face_recognizer = FaceRecognizer()
    emotion_classificator = EmotionClassificator()

    def __init__(self):
        self.raw_images = dict()
        self.processed_images = []
        self.plots = []
    
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

    def load_image(self, filename: str, content) -> None:
        nparr = np.frombuffer(content, np.uint8)
        self.raw_images[filename]=(cv2.imdecode(nparr, 1))

    def process_images(self):
        self.processed_images.clear()
        for name, image in self.raw_images.items():
            processed_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(processed_image)

            faces, coordinates = self.face_recognizer.recognize_faces(image=image)
            emotions = self.emotion_classificator.classify_emotions(data=faces)

            emots = {e: 0 for e in EMOTIONS}
            for t, l in zip(coordinates, emotions):
                coords = {}  # x, y, width, height
                box_and_labels = {}  # box, label
                coords['x'], coords['y'], coords['width'], coords['height'] = int(t[0]), int(t[1]), int(t[2]), int(t[3])
                box_and_labels["box"], box_and_labels["label"] = coords, l
                emots[l] += 1
                draw.rectangle((coords['x'], coords['y'], coords['x'] + coords['width'], coords['y']+coords['height']), outline='red')
            print(emots)
            self.processed_images.append(ProcessedImage(name, processed_image, emots))
        self.build_plots()


    def build_plots(self):
        self.plots.clear()
        emots = {e: 0 for e in EMOTIONS}
        for image in self.processed_images:
            for emot, count in image.emotions.items():
                emots[emot] += count

        plt.bar(emots.keys(), emots.values())
        plt.xlabel('Эмоции')
        plt.ylabel('Количество')
        plot_image = FigureCanvasAgg(plt.gcf())
        plot_image.draw()
        plot_image = np.array(plot_image.renderer.buffer_rgba())
        plot_image = Image.fromarray(plot_image)
        data = {
            'Max': np.max(emots.values()),
            'Min': np.min(emots.values()),
        }
        self.plots.append(Plot('counts.png', plot_image, data))

    def get_plots(self):
        return self.plots

    def get_processed_images(self):
        return self.processed_images


class Plot:
    def __init__(self, name, image, data: dict):
        self.name = name
        self.image = image
        self.data = data

class ProcessedImage:
    def __init__(self, name, image, emotions: dict):
        self.name = name
        self.image = image
        self.emotions = emotions
