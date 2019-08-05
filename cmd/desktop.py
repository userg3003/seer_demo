from internal import compose
from pkg import clf as clf_pkg
from pkg.io import readers
from pkg.utils import inference
from pkg.utils import visualizer

from keras import models as keras_models
import numpy as np


def main():
    kwargs = compose.desktop()

    # loading models
    face_detection = inference.load_detection_model(kwargs['face_detection_model_path'])
    emotion_classifier = keras_models.load_model(kwargs['emotion_model_path'], compile=False)

    reader = readers.VideoFileReader(kwargs['video_path'])
    clf = clf_pkg.EmotionClassifier(
        reader=reader,
        offsets=kwargs['emotion_model']['offset'],
        face_detector=face_detection,
        emotion_detector=emotion_classifier,
    )
    seconds = []
    distributions = []
    try:
        for item in clf:
            sec, distr = item
            seconds.append(sec)
            distributions.append(distr)
        return seconds, distributions
    except KeyboardInterrupt:
        pass
    visualizer.build_report_image(
        seconds=np.array(seconds),
        distributions=np.array(distributions),
        labels=clf.get_labels(),
        path=kwargs['image_report_path'],
    )


if __name__ == '__main__':
    main()
