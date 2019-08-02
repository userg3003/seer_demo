import time
import io
import threading
import cv2
# import picamera
import sys
import os
from multiprocessing import Process, current_process


def trace1(file: object, lineno: object, name: object, pid: object, ppid: object, pr_name: object, dop: object = "") -> object:
    print(f"\t\t\t@#$%| {file} {lineno}\t{name}\tpid={pid} \tparent pid={ppid}\t{pr_name} | {dop}")
    ...


trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)

import logging


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    frame1 = None
    last_access = 0  # time of last client access to the camera
    cap = None
    logging.debug("")
    trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)

    def initialize(self):
        trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
        logging.debug("")
        if Camera.thread is None:
            # start background frame thread
            trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
            logging.debug("")
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                # trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
                logging.debug("")
                time.sleep(0)

    def get_frame(self):
        logging.debug("")
        trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
        logging.debug("")
        cls.cap = cv2.VideoCapture('demo.mp4')

        # Check if camera opened successfully
        if cls.cap.isOpened() == False:
            print("Error opening video stream or file")
            logging.debug("")
            return
        # cv2.Get  GetCaptureProperty(cls.cap, cv2.CV_CAP_PROP_POS_MSEC)
        # cv2.SetCaptureProperty(cls.cap, cv2.CV_CAP_PROP_POS_MSEC, 90000)

        trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
        # time.sleep(2)
        count = 0
        while cls.cap.isOpened():
            logging.debug("")
            # trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
            # Capture frame-by-frame
            try:
                ret, cls.frame1 = cls.cap.read()
            except Exception:
                print(f'Error .............')

            # cls.frame1 = cv2.QueryFrame(cls.cap)
            try:
                # cls.frame = cv2.EncodeImage('.jpg', cls.frame1).tostring()
                ret, fr = cv2.imencode('.jpg', cls.frame1)
                cls.frame = fr.tostring()

            except Exception:
                print(f'Error .............')
            # print(f'Read a new frame{count}:{ret} ')
            count += 1
            # if not ret:
            #     break
        cls.thread = None



