import logging

from keras.models import model_from_json
import matplotlib.pyplot as plt

from src import settings

import numpy as np
import cv2


logger = logging.getLogger(__name__)


class EmotionClassificator:
    _EMOTIONS = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']
    _WEIGHTS_PATH = './src/emotion_classificator/weights/modelAugClass1SWFinned.h5'
    _MODEL_PATH = './src/emotion_classificator/weights/modelAugClass1SWFinned.json'
    
    def __init__(self) -> None:
        self.model = self._load_model()

    def classify_emotions(self, data):
        predict_dataset = []
        for f in data:
            np_image = self.convert_image(f)
            predict_dataset.append(np_image)
        
        norm_dataset = self.normalize_dataset(predict_dataset)
        x_predict = self.reshape_dataset(norm_dataset)
        predicred_emotions = self.model.predict(x=x_predict)

        emotion_classification = self.make_classification(results=predicred_emotions, X_predict=x_predict)        
        return emotion_classification

    def _load_model(self):
        with open(self._MODEL_PATH, 'r') as f:
            model_content = f.read()    
        
        model = model_from_json(model_content)
        model.load_weights(self._WEIGHTS_PATH)
        
        logger.info("Loaded model from disk")
        return model

    def convert_image(self, image):
        ''' Resize image into size 48x48, convert into numpy array and return it '''
        np_image = cv2.resize(image, dsize=(48, 48), interpolation=cv2.INTER_CUBIC)
        
        if settings.DEBUG:
            EmotionClassificator._show_converted_image(np_image)
        
        return np_image

    def normalize_dataset(self, dataset):
        ''' Normalize all images in the predict dataset '''
        for i in range(len(dataset)):
            r = cv2.normalize(dataset[i], None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            dataset[i] = r
            
        return dataset

    def reshape_dataset(self, dataset):
        ''' Return a reshaped dataset '''
        new_data = np.reshape(dataset ,(len(dataset), 48,48,3))
        
        if settings.DEBUG:
            logger.info(new_data.shape)
        
        return new_data

    @staticmethod
    def _show_converted_image(image):
        ''' Show an image, it`s mode and shape '''
        print(image.shape)
        plt.imshow(image, interpolation='nearest')
        plt.show()

    def make_classification(self, results, X_predict):
        ''' Return a final predict labels list '''
        final_predict = []
        label = None
        show_cnt = 0
        for r, img in zip(results, X_predict):
            emotion_number = list(r).index(max(r))
            label = EmotionClassificator._EMOTIONS[emotion_number]
    
            final_predict.append(label)
        return final_predict
