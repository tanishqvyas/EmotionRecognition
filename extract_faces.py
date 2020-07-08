# detecting faces in images, extracting the image slice and storing
from mtcnn import MTCNN
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
detector = MTCNN()
ind=10000
for i in range(len(image_list)):
    img=image_list[i]
    faces = detector.detect_faces(img)
    for f in faces:
        x,y,w,h = f.get('box')
        ROI = img[y:y+h, x:x+w]
        try:
            roi_resized = cv2.resize(ROI,(48,48),interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(roi_resized,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(str(ind)+'.jpg',gray)
            print("kiya",ind)
            ind+=1
        except:
            pass