import cv2
import os


def path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


vid_cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

Student_id = input("Enter face ID: ")
Student_name = input("Enter face name: ")
count = 0

path_exists("training_data/")

while True:
    _, frame = vid_cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
        count += 1
        cv2.imwrite("training_data/Person." + str(Student_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.putText(frame, "Data collected " + str(count) + " out of 100", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    elif count >= 100:
        break

vid_cam.release()
cv2.destroyAllWindows()