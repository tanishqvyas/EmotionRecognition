import time
start_time = time.time()
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import os
import glob
from mtcnn import MTCNN

log = open("log.txt","w+")
# Importing the MTCNN detector to detect faces
detector = MTCNN()

os.system("cls")
print("--- Time taken to load tensorflow = %s seconds ---" % (time.time() - start_time))

ext = input("Enter the image extension : ")

# Start Time
start_time = time.time()

# Path to the emotion detection model
model_path = os.path.join("model","emotional_fool.h5")
classifier =load_model(model_path)

class_labels = ['Angry','Happy','Neutral','Sad','Surprise'] # Remember to keep in alphabetical order
count = []

for emt in class_labels:
    os.chdir(emt)
    images = glob.glob("*"+ext)
    count.append(len(images))
    for img in images:
        img_name=img
        img = cv2.imread(img)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Get a dictionary of all faces
        faces = detector.detect_faces(img)
        # For every face in the faces detected in the current frame
        for face in faces:            
            # Get the confidence value of the 'f' being a face
            if face.get('confidence')>=0.9:
                # Get the co-ordinates of the cropped area wherein face lies
                x,y,w,h = face.get('box')
                # Draw a Rectangle
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
                roi_gray = gray[y:y+h,x:x+w]
                try:
                    roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
                except:
                    print("--- %s seconds ---" % (time.time() - start_time))
                if np.sum([roi_gray])!=0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi,axis=0)

                # make a prediction on the ROI, then lookup the class

                    preds = classifier.predict(roi)[0]
                    label=class_labels[preds.argmax()]
                    label_position = (x,y-5)
                    cv2.putText(img,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

                else:
                    cv2.putText(img,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.imwrite(label+img_name+".jpg", img)
    os.chdir("..")

end_time = time.time()

result = []
for emt in class_labels:
    os.chdir(emt)
    res = glob.glob(emt+"*") 
    result.append(len(res))
    os.chdir("..")

os.system("cls")

print("Model used : ",model_path[5:])
for i in range(5):
    print(class_labels[i],result[i],":",count[i])
    log.write(str(class_labels[i]+" "+str(result[i])+":"+str(count[i])+"\n"))
print("--- Total time take =  %s seconds ---" % (end_time - start_time))
print("--- Total Accuracy = %s percent" %((sum(result)/sum(count))*100))
print("Note : This program calculates the time for both detecting faces and identifying emotions")
log.close()
import clear
time.sleep(20)
