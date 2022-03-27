import os
import numpy as np
from PIL import Image
import cv2
import pickle

from numpy.core.numeric import identity
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,"images_check")

cur_id = 0
label_ids = {}
y_labels = []
x_train = []

identifier = cv2.face_LBPHFaceRecognizer.create()

faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
for root,dirs,files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root,file)
            label = os.path.basename(root)
            
            if label in label_ids:
                pass
            else:
                label_ids[label] = cur_id
                cur_id+=1
            id_ = label_ids[label]
            image = Image.open(path)
            final_img = image.resize((550,550),Image.ANTIALIAS)
            array_image = np.array(final_img)
            faces = faceCascade.detectMultiScale(array_image)
            for (x,y,w,h) in faces:
                roi_color = array_image[y:y+h, x:x+w]
                x_train.append(roi_color)
                y_labels.append(id_)


with open("labels.pickle","wb") as f:
    pickle.dump(label_ids,f)

identifier.train(x_train,np.array(y_labels))
identifier.save("faces_training.yml")