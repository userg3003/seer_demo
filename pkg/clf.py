import typing

import cv2
import numpy as np
from tqdm import tqdm

from pkg.io import readers
from pkg.utils import inference
from pkg.utils import datasets
from pkg.utils.preprocessor import preprocess_input


class EmotionClassifier:
    def __init__(self, reader: readers.Reader, offsets: typing.Tuple[int, int], face_detector, emotion_detector,
                 graph=None):
        self.__reader = reader
        self.__face_detector = face_detector
        self.__emotion_detector = emotion_detector
        self.__emotion_offsets = offsets
        self.__emotion_target_size = self.__emotion_detector.input_shape[1:3]
        self.__graph = graph

    def __apply_offsets(self, face_coordinates):
        x, y, width, height = face_coordinates
        x_off, y_off = self.__emotion_offsets
        return x - x_off, x + width + x_off, y - y_off, y + height + y_off

    def __extract_best_face(self, faces):
        i_max = None
        max_delta = 0
        for i, face_coordinates in enumerate(faces):
            x1, x2, y1, y2 = self.__apply_offsets(face_coordinates)
            non_negative = x2 > 0 and x1 > 0 and y1 > 0 and y2 > 0
            cond = max(x2 - x1, y2 - y1) >= max_delta and min(x2 - x1, y2 - y1) > 0
            if cond and non_negative:
                i_max = i
        return i_max

    def __get_distr(self, gray_face):
        if self.__graph is not None:
            with self.__graph.as_default():
                # we don't use neutral emotion (last column)
                distr = self.__emotion_detector.predict(gray_face)[0, :-1]
        else:
            # we don't use neutral emotion (last column)
            distr = self.__emotion_detector.predict(gray_face)[0, :-1]
        distr = self.__distribution_norm(distr)
        return distr

    @staticmethod
    def __distribution_norm(distr):
        return (distr.T / distr.T.sum(axis=0)).T

    def flush(self):
        self.__reader.flush()

    @staticmethod
    def get_labels():
        # we don't use neutral emotion
        labels = datasets.get_labels('fer2013')
        labels = [v for k, v in sorted(labels.items(), key=lambda el: el[0]) if v != 'neutral']
        return labels

    def __iter__(self):
        for i, item in tqdm(enumerate(self.__reader)):
            second, bgr_frame = item
            gray_image = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
            faces = inference.detect_faces(self.__face_detector, gray_image)

            i_max = self.__extract_best_face(faces)
            # we don't found any faces
            if i_max is None:
                yield second, np.zeros(len(self.get_labels()))
                continue

            x1, x2, y1, y2 = self.__apply_offsets(faces[i_max])
            gray_face = gray_image[y1:y2, x1:x2]
            gray_face = cv2.resize(gray_face, self.__emotion_target_size)
            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            distr = self.__get_distr(gray_face)
            yield second, distr
