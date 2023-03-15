
import cv2
import os
import numpy as np
from PIL import Image

def path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
print("Training started")
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

    print("imagepaths",imagePaths)
    faceSamples=[]
    ids = []
    print("faceSamples","ids",faceSamples,ids)
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
faces,ids = getImagesAndLabels('training_data')

recognizer.train(faces, np.array(ids))

path_exists('saved_model/')
recognizer.write('saved_model/s_model.yml')
print('Training Finish')
