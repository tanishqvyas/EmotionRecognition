# script to segregate training and validation data

import cv2
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images
image_list = load_images_from_folder("Sad")
c1=0
c2=0
i=0

for i in range(len(image_list)):
    if(i%10==0):
        c1+=1
        path="/home/mohit/EmotionRecognition/data/validation/Sad"
        cv2.imwrite(os.path.join(path,'n'+str(i+4000)+'.jpg'),image_list[i])
    else:
        c2+=1
        path="/home/mohit/EmotionRecognition/data/train/Sad"
        cv2.imwrite(os.path.join(path,'n'+str(i+20000)+'.jpg'),image_list[i])
print(c1,c2)