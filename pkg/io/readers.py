import cv2


class Reader:
    def __iter__(self):
        raise NotImplemented('this method not implemented in base class')

    def flush(self):
        raise NotImplemented('this method not implemented in base class')


class VideoFileReader(Reader):
    def __init__(self, path):
        self.__path = path
        self.__capture = None

    def __get_time(self):
        return self.__capture.get(cv2.CAP_PROP_POS_MSEC) / 1000

    def flush(self):
        self.__capture = cv2.VideoCapture(self.__path)

    def __iter__(self):
        self.flush()
        ok, bgr_image = self.__capture.read()
        while ok:
            yield self.__get_time(), bgr_image
            ok, bgr_image = self.__capture.read()
