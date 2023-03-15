import csv
import cv2
import numpy as np
import os
import datetime

def path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

recognizer = cv2.face.LBPHFaceRecognizer_create()
path_exists("saved_model/")
recognizer.read('saved_model/s_model.yml')
cascade = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascade)
font = cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0)

detected_ids = []

csv_file = open('attendance.csv', 'a', newline='')
csv_writer = csv.writer(csv_file)

if os.stat('attendance.csv').st_size == 0:
    csv_writer.writerow(['ID', 'Name','Date and Time'])

while True:

    ret, frame =cam.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
        Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        if Id == 1:
            name = "Ajay"
            confidence_level = round(100 - confidence, 2)
        elif Id == 2 :
            name = "Sajith"
            confidence_level = round(100 - confidence, 2)
        elif Id == 3:
            name = "Mohammad"
            confidence_level = round(100 - confidence, 2)
        elif Id == 4:
            name = "Sajmal"
            confidence_level = round(100 - confidence, 2)
        elif Id == 5:
            name = "jermy"
            confidence_level = round(100 - confidence, 2)
        elif Id == 6:
            name = "Sayooj"
            confidence_level = round(100 - confidence, 2)
        elif Id == 7:
            name = "Sooraj"
            confidence_level = round(100 - confidence, 2)
        elif Id == 8:
            name = "Eashwar"
            confidence_level = round(100 - confidence, 2)
        else:
            name = "Unknown"
            confidence_level = round(100 - confidence, 2)

        if Id not in detected_ids:
            detected_ids.append(Id)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            csv_writer.writerow([Id, name, current_time])

        cv2.rectangle(frame, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
        cv2.putText(frame, name + ' ' + str(confidence_level) + '%', (x,y-40), font, 1, (255,255,255), 3)

    cv2.imshow('im',frame)


    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cam.release()
csv_file.close()
cv2
