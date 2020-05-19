from abc import ABC, abstractclassmethod, abstractproperty
import math
import numpy as np
import time
from collections import Counter, defaultdict
from keras.models import Sequential, load_model
import keras
import keras.backend as K
import cv2
import os
import tensorflow as tf

class IStrategySearchDistance(ABC):

    @abstractclassmethod
    def execute(self, x1, y1, x2, y2): pass


class EuclideanDistanceStrategy(IStrategySearchDistance):

    def execute(self, x1, y1, x2, y2):
        return math.sqrt(pow((x1-x2),2)+pow((y1-y2),2))


class Detector:
    def __init__(self):
        self.background = None
        self.MIN_AREA = 0
        self.MAX_AREA = 0
        self.TIME_TO_DETECT = 0
        self.TIME_TO_WARN = 0
        self.TIME_TO_FORGET = 0
        self.BIGGEST_SIZE = 0
        self.DISTANCE_TO_UNDETECT = 0
        self.model = None
        self.DISTANCE_STRATEGY = None
        self.dimentions = None
        self.first_gray = None
        self.track_temp = []
        self.track_master = []
        self.track_temp2 = []
        self.temp_detected = [] # --
        self.detected_bags = [] # --
        self.top_contour_dict = defaultdict(int)
        self.obj_detected_dict = defaultdict(int)
        self.bags_centroids = defaultdict(int)
        self.frameno = 0
        self.consecutiveFrame = 20
        self.undetect_centroids = []
    
    def __str__(self):
        return str(self.MIN_AREA) + " "+ str(self.MAX_AREA) + " "+ str(self.TIME_TO_DETECT) + " "+ str(self.TIME_TO_WARN) + " "+ str(self.TIME_TO_FORGET) + " "+ str(self.BIGGEST_SIZE) + " "+ str(self.DISTANCE_TO_UNDETECT) + " " + str(type(self.model)) + str(type(self.DISTANCE_STRATEGY))


    def checkDifferent(self, cap):
        gray_frame = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        difference = cv2.absdiff(self.first_gray, gray_frame)
        _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        kernel2 = np.ones((3, 3), np.uint8)
        difference = cv2.morphologyEx(difference, cv2.MORPH_CLOSE, kernel2, iterations=2)

        return difference


    def checkFrame(self, cap):

        frame = cap
        gray_frame = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        difference = cv2.absdiff(self.first_gray, gray_frame)
        _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        kernel2 = np.ones((3, 3), np.uint8)
        difference = cv2.morphologyEx(difference, cv2.MORPH_CLOSE, kernel2, iterations=2)

        if len(self.undetect_centroids) != 0:
            for centroid in self.undetect_centroids:
                cv2.line(difference, (centroid[0], centroid[1]), (centroid[2], centroid[3]), (255, 255, 255), 5)

        self.frameno = self.frameno + 1

        contours, _ = cv2.findContours(difference, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        tempContours = []
        human_move_centroids = []
        self.undetect_centroids.clear()

        for contour in contours:

            moments = cv2.moments(contour)
            if moments['m00'] == 0:
                pass
            else:
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])

                (x, y, w, h) = cv2.boundingRect(contour)

                if x == 0 or y == 0 or x + w == self.dimentions[1] or y + h == self.dimentions[0]:
                    continue

                if cv2.contourArea(contour) > self.BIGGEST_SIZE:
                    human_move_centroids.append([cx, cy])

                if cv2.contourArea(contour) < self.MIN_AREA or cv2.contourArea(contour) > self.MAX_AREA:
                    pass
                else:
                    tempContours.append(contour)
                
                    sumcxcy = cx + cy

                    self.track_temp.append([cx + cy, self.frameno])
                    self.track_master.append([cx + cy, self.frameno])

                    countuniqueFrame = set(j for i, j in self.track_master)

                    if len(countuniqueFrame) > self.consecutiveFrame or False:
                        mainframeno = min(j for i, j in self.track_master)
                        for i, j in self.track_master:
                            if j != mainframeno:
                                self.track_temp2.append([i, j])
                    
                        self.track_master = list(self.track_temp2)
                        self.track_temp2 = []
                    
                    countcxcy = Counter(i for i, j in self.track_master)
                    for i, j in countcxcy.items():
                        if j >= self.consecutiveFrame:
                            self.top_contour_dict[i] += 1
                    
                    if sumcxcy in self.top_contour_dict:
                        if self.top_contour_dict[sumcxcy] > self.TIME_TO_DETECT:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                            self.bags_centroids[sumcxcy] = [cx, cy]
                            self.obj_detected_dict[sumcxcy] = self.frameno

                        if self.top_contour_dict[sumcxcy] > self.TIME_TO_WARN:
                            crop_img = frame[y:y + h, x:x + w]
                            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                            crop_img = cv2.resize(crop_img, (28, 28))
                            crop_img = np.invert(crop_img)
                            crop_img = (crop_img.astype(np.float32)) / 255.0
                            crop_img = crop_img.reshape(1, 28, 28, 1)
                            with keras.backend.get_session().graph.as_default():
                                prediction = self.model.predict(crop_img)
                            #K.clear_session()
                            resClass = np.argmax(prediction[0])
                            if resClass == 8:
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                                self.obj_detected_dict[sumcxcy] = self.frameno
                                self.bags_centroids[sumcxcy] = [cx, cy]
                                resPredict = int(max(prediction[0]) * 100)
                                tempClass = str(resPredict) + '%'
                                cv2.putText(frame, tempClass, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA, False)
                            prediction = None
                            

        for i, j in list(self.obj_detected_dict.items()):
            for ch in human_move_centroids:
                dist = self.DISTANCE_STRATEGY.execute(ch[0], ch[1], self.bags_centroids[i][0], self.bags_centroids[i][1])
                if dist < self.DISTANCE_TO_UNDETECT:
                    cv2.line(frame, (ch[0], ch[1]), (self.bags_centroids[i][0], self.bags_centroids[i][1]), (255, 0, 0), 5)
                    self.undetect_centroids.append([ch[0], ch[1], self.bags_centroids[i][0], self.bags_centroids[i][1]])
                    if self.frameno - self.obj_detected_dict[i] > self.TIME_TO_FORGET:
                        self.obj_detected_dict.pop(i)
                        self.top_contour_dict[i] = 0
    
        return frame


class IBuilderDetector(ABC):

    @abstractproperty
    def detector(self) -> None:
        pass

    @abstractclassmethod
    def reset(self) -> None:
        pass

    @abstractclassmethod
    def setConvolutionModel(self) -> None:
        pass

    @abstractclassmethod
    def setMinArea(self, area) -> None:
        pass

    @abstractclassmethod
    def setMaxArea(self, area) -> None:
        pass

    @abstractclassmethod
    def setTimeToDetect(self, time) -> None:
        pass

    @abstractclassmethod
    def setTimeToWarn(self, time) -> None:
        pass

    @abstractclassmethod
    def setTimeToForget(self, time) -> None:
        pass

    @abstractclassmethod
    def setBiggestSize(self, size) -> None:
        pass

    @abstractclassmethod
    def setDistanceToUndetect(self, distance) -> None:
        pass

    @abstractclassmethod
    def setDistanceStrategy(self, distance_strategy) -> None:
        pass


class BuilderDetector(IBuilderDetector):

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._detector = Detector()

    @property
    def detector(self) -> Detector:
        detector = self._detector
        self.reset()
        return detector

    def setConvolutionModel(self) -> None:
        self._detector.model = keras.models.load_model('D:\DiplomDetect\AbadDetect\detector\detect_models\convolutional_fashion_model.h5')
    
    def setMinArea(self, area) -> None:
        self._detector.MIN_AREA = area

    def setMaxArea(self, area) -> None:
        self._detector.MAX_AREA = area

    def setTimeToDetect(self, time) -> None:
        self._detector.TIME_TO_DETECT = time

    def setTimeToWarn(self, time) -> None:
        self._detector.TIME_TO_WARN = time

    def setTimeToForget(self, time) -> None:
        self._detector.TIME_TO_FORGET = time

    def setBiggestSize(self, size) -> None:
        self._detector.BIGGEST_SIZE = size

    def setDistanceToUndetect(self, distance) -> None:
        self._detector.DISTANCE_TO_UNDETECT = distance

    def setDistanceStrategy(self, distance_strategy) -> None:
        self._detector.DISTANCE_STRATEGY = distance_strategy
    
    def setBackground(self, background) -> None:
        self._detector.background = background
        frs_gray = cv2.cvtColor(self._detector.background, cv2.COLOR_BGR2GRAY)
        frs_gray = cv2.GaussianBlur(frs_gray, (21, 21), 0)
        self._detector.first_gray = frs_gray
    
    def setDimentions(self, dimentions) -> None:
        self._detector.dimentions = dimentions

