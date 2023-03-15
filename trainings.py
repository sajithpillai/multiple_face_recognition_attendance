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
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def getImagesAndLabels(path):
    faceSamples = []
    ids = []
    #print("faceSamples:", faceSamples, "ids:", ids)

    for foldername in os.listdir(path):
        folderpath = os.path.join(path, foldername)
        if not os.path.isdir(folderpath):
            continue

        id = int(foldername.split('_')[1])
        print("id is",id)

        for filename in os.listdir(folderpath):
            if not filename.endswith('.jpg'):
                continue

            imagePath = os.path.join(folderpath, filename)
            #print("imagePath:",imagePath)
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')

            faces = detector.detectMultiScale(img_numpy)
            #print("faces:", faces)
            if len(faces) == 0:
                continue
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)

    #print("ids before return",ids)

    return faceSamples, ids


faces, ids = getImagesAndLabels('Dataset/faces/')
print("ids:", ids)

recognizer.train(faces, np.array(ids))

path_exists('saved_model/')
recognizer.write('saved_model/s_model.yml')

print('Training Finish')
