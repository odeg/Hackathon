# Import required modules
from ast import If
import cv2 as cv
import math
import time
import matplotlib.pyplot as cv2_imshow
from datetime import datetime
from datetime import timedelta 

from pushbullet import Pushbullet
from sqlalchemy import true

API_KEY = "o.t9HTbcNGkW67EzEh8q1Xr5349q0lFyJa"
#warning_time = 0

# pb = Pushbullet(API_KEY)
# push =pb.push_note("Sujeto no identificado detectado en zona prohibida","alo")
# import argparse

def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes

faceProto = "modelNweight/opencv_face_detector.pbtxt"
faceModel = "modelNweight/opencv_face_detector_uint8.pb"

ageProto = "modelNweight/age_deploy.prototxt"
ageModel = "modelNweight/age_net.caffemodel"

genderProto = "modelNweight/gender_deploy.prototxt"
genderModel = "modelNweight/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# Load network
ageNet = cv.dnn.readNet(ageModel, ageProto)
genderNet = cv.dnn.readNet(genderModel, genderProto)
faceNet = cv.dnn.readNet(faceModel, faceProto)

padding = 20
global warning_time
def age_gender_detector(frame):
    mensaje = False
    # Read frame
    t = time.time()
    frameFace, bboxes = getFaceBox(faceNet, frame)
    for bbox in bboxes:
        # print(bbox)
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]

        blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        # print("Gender Output : {}".format(genderPreds))
        #print("Gender : {}, conf = {:.3f}".format(gender, genderPreds[0].max()))

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        index_ageList = agePreds[0].argmax()
        # if agePreds[0].argmax()>3:
        #     index_ageList = agePreds[0].argmax()
        # else:
        #     index_ageList = 0
        # print("Index" + str(index_ageList))
        #print("Age Output : {}".format(agePreds))
        #print("Age : {}, conf = {:.3f}".format(age, agePreds[0].max()))

        label = "{},{}".format(gender, age)
        frameFace = cv.putText(frameFace, label, (bbox[0], bbox[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv.LINE_AA)
        frameFace = cv.rectangle(frameFace, (bbox[0],bbox[1]) , (bbox[2],bbox[3]), (255,0,0), 2)
        
        #warning_time = None 
        if int(index_ageList) > 2 :
            mensaje = True
            # pb = Pushbullet(API_KEY)
            # push =pb.push_note("Advertencia", "Sujeto no identificado detectado en zona restringida")
            # current_time = datetime.now()
            # try:
            #     if current_time > (warning_time + timedelta(seconds=30)):
            #         print("Dentro del if" + str(warning_time))
            #         pb = Pushbullet(API_KEY)
            #         push =pb.push_note("Advertencia", "Sujeto no identificado detectado en zona restringida")
            #         warning_time = current_time
            #     else:
            #         pass
            # except Exception as e:
            #     print(e)
            #     warning_time = current_time
            #     pb = Pushbullet(API_KEY)
            #     push =pb.push_note("Advertencia", "Sujeto no identificado detectado en zona restringida")
                # pb = Pushbullet(API_KEY)
                # push =pb.push_note("Advertencia", "Sujeto no identificado detectado en zona restringida")
                # print("Dentro del except " + str(warning_time))
            # pb = Pushbullet(API_KEY)
            # push =pb.push_note("Advertencia", "Sujeto no identificado detectado en zona prohibida")
        # #         push =pb.push_note("Advertencia", "Sujeto no identificado detectado en zona prohibida")
        # #     if warning_time == None:
        # #         warning_time = datetime.now()
        # #         #warning_time = now.strftime("%H:%M:%S")
        # #         pb = Pushbullet(API_KEY)
        # #         push =pb.push_note("Advertencia", "Sujeto no identificado detectado en zona prohibida")
        # #     current_time = datetime.now()
        # #     #current_time = now.strftime("%H:%M:%S")
        # #     if current_time > (warning_time + timedelta(seconds=30)):
        # #         pb = Pushbullet(API_KEY)
        # #         push =pb.push_note("Advertencia", "Sujeto no identificado detectado en zona prohibida")
        # #         warning_time = None
    return frameFace, mensaje
cap = cv.VideoCapture(0)
ret, frame = cap.read()
frame_height, frame_width, _ = frame.shape
out = cv.VideoWriter('output.avi',cv.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
print("Processing Video...")

while cap.isOpened():
    ret, frame = cap.read()
# frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
# cv.imshow('frame',frame)
    if not ret:
        out.release()
        break
    #time.sleep(30)
    output= age_gender_detector(frame)
    cv.imshow('frame',output[0])
    out.write(output[0])
    envio = output[1]
    if envio:
        pb = Pushbullet(API_KEY)
        push =pb.push_note("Advertencia", "Sujeto no identificado detectado en zona restringida")
        time.sleep(10)
    k = cv.waitKey(30)
    if k ==27:
        break
out.release()
print("Done processing video")
cv.destroyAllWindows()