from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import numpy as np
import cv2
import time
from detector.detectModels import *
import io
from PIL import Image

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
import base64
from authmanage.models import Camera, DetectedObj

detectors = []

strategy = EuclideanDistanceStrategy()
builderDetector = BuilderDetector()

'''
camera = cv2.VideoCapture(0)

strategy = EuclideanDistanceStrategy()

builderDetector = BuilderDetector()


builderDetector.setMinArea(500)
builderDetector.setMaxArea(10000)
builderDetector.setTimeToDetect(100)
builderDetector.setConvolutionModel()
builderDetector.setTimeToWarn(200)
builderDetector.setTimeToForget(50)
builderDetector.setBiggestSize(15000)
builderDetector.setDistanceToUndetect(200)
builderDetector.setDistanceStrategy(strategy)

_, test_frame = camera.read()
dimentions = test_frame.shape
time.sleep(4)
_, first_frame = camera.read()

builderDetector.setDimentions(dimentions)
builderDetector.setBackground(first_frame)

detector = builderDetector.detector

del(camera)
'''


def get_frame():

    camera =cv2.VideoCapture(0) 

    while True:
        _, img = camera.read()
        #img = detector.checkFrame(img)
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
    
    del(camera)
    
def indexscreen(request): 
    try:
        template = "detect.html"
        return render(request,template)
    except HttpResponseServerError:
        print("error")

@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"


def decodeFrame(frame):
    encoded_data = frame.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def encodeFrame(frame):
    retval, buffer = cv2.imencode('.jpeg', frame)
    res_string = base64.b64encode(buffer)
    return res_string


@api_view(["POST"])
@parser_classes([JSONParser])
def detectFrame(frame):
    try:
        if frame is None:
            return Response({'recieveData' : "Camera is not ready"})
        if detectors != []:
            codeFrame = frame.data['encodedFrame']
            img = decodeFrame(codeFrame)
            res = detectors[0][1].checkFrame(img)
            res_string = encodeFrame(res)
            return Response({'recieveData': res_string })

        return Response({'recieveData': "Detectors didn't created" })
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@parser_classes([JSONParser])
def getBack(background):
    try:
        codeFrame = background.data['encodedFrame']
        idTemp = background.data['idCam']
        image = decodeFrame(codeFrame)
        path = os.path.dirname(os.path.abspath(__file__))
        path = path.replace("\detector", "\media\\backgrounds\\")
        path = path + str(idTemp) + '.jpeg'
        cv2.imwrite(path, image)
        camera = Camera.objects.filter(id = idTemp).update(background = path)
        if detectors != []:
            for detector in detectors:
                if detector[0] == idTemp:
                    backgroundImage = cv2.imread(path)
                    detector[1].background = backgroundImage
                    break
        return Response({ 'success': "background updated" })
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@parser_classes([JSONParser])
def getDetectedImage(detectedId):
    try:
        idNumber = detectedId.data['recievedId']
        print(idNumber)
        detectedTemp = DetectedObj.objects.get(id=idNumber)
        urlDetectedImage = detectedTemp.image
        imageDetected = cv2.imread(urlDetectedImage)
        res_string = encodeFrame(imageDetected)
        return Response({ 'encoded_frame' : res_string })
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@parser_classes([JSONParser])
def createDetectors(recivedData):
    try:
        cameras = recivedData.data
        detectors.clear()
        
        for camera in cameras:
            builderDetector.setMinArea(camera['min_area'])
            builderDetector.setMaxArea(camera['max_area'])
            builderDetector.setTimeToDetect(camera['time_to_detected'])
            builderDetector.setTimeToWarn(camera['time_to_warn'])
            builderDetector.setTimeToForget(camera['time_to_forget'])
            builderDetector.setUser(camera['user'])
            builderDetector.setBiggestSize(camera['biggest_size'])
            builderDetector.setDistanceToUndetect(float(camera['distance_to_undetect']))
            builderDetector.setConvolutionModel()
            backgroundDetectorImage = cv2.imread(camera['background'])
            dimentions = backgroundDetectorImage.shape
            builderDetector.setDistanceStrategy(strategy)
            builderDetector.setDimentions(dimentions)
            builderDetector.setBackground(backgroundDetectorImage)
            detectors.append([camera['id'], builderDetector.detector])
        
        return Response({ 'result' : "Detectors created" })
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
