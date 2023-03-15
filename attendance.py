import os
import csv
import numpy as np
from datetime import date
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, redirect


#### Defining Flask App
app = Flask(__name__)

def path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def datetoday():
    return date.today().strftime("%m_%d_%y")

def datetoday2():
    return date.today().strftime("%d-%B-%Y")

def totalreg():
    return len(os.listdir('Dataset/faces'))

def path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

vid_cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Student_id = input("Enter face ID: ")
count = 0

path_exists("training_data/")





@app.route('/')
def home():
    return render_template('home.html')

#### This function will run when we add a new user
@app.route('/add', methods=['GET', 'POST'])
def add_students():
    root_foler = "Dataset/faces/"


    student_id = request.form['newuserid']
    student_name = request.form['newusername']

    path = os.path.join(root_foler, f"{student_name}_{student_id}")
    print(path)
    if not os.path.isdir(path):
        os.makedirs(path)
    count = 0
    while True:
        _, frame = vid_cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            filename = os.path.join(path, f"{student_name}_{count}.jpg")
            cv2.imwrite(filename, gray[y:y + h, x:x + w])
            cv2.putText(frame, f"Data collected {count} out of 100", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        2, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        elif count >= 100:
            break

    vid_cam.release()
    cv2.destroyAllWindows()
    return render_template('home.html')
@app.route('/start', methods=['GET'])
def start():

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

    folder_path = "Dataset/faces/"
    delimiter = "_"
    student_dict = {}
    print(student_dict)

    for folder_name in os.listdir(folder_path):
        # split the folder name by the delimiter and get the student ID and name
        student_name, student_id = folder_name.split(delimiter)
        print(student_id, student_name)
        # add the student ID and name to the dictionary
        student_dict[student_id] = student_name
        # append the dictionary with the student ID and name
        student_dict = {**student_dict, student_id: student_name}

    print(student_dict)

    csv_file = open('attendance.csv', 'a', newline='')
    csv_writer = csv.writer(csv_file)

    if os.stat('attendance.csv').st_size == 0:
        csv_writer.writerow(['ID', 'Name', 'Date and Time'])

    while True:

        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 4)
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            print("id,confidence is", Id, confidence)
            if str(Id) in student_dict:
                name = student_dict[str(Id)]
                print("name is", name)
                confidence_level = round(100 - confidence, 2)
            else:
                name = "Unknown"
                confidence_level = round(100 - confidence, 2)

            if Id not in detected_ids:
                detected_ids.append(Id)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                csv_writer.writerow([Id, name, current_time])

            cv2.rectangle(frame, (x - 22, y - 90), (x + w + 22, y - 22), (0, 255, 0), -1)
            cv2.putText(frame, name + ' ' + str(confidence_level) + '%', (x, y - 40), font, 1, (255, 255, 255), 3)

        cv2.imshow('im', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cam.release()
    csv_file.close()
    cv2
    return render_template('home.html', totalreg=totalreg(),
                           datetoday2=datetoday2())

if __name__ == '__main__':
    app.run(debug=True)
