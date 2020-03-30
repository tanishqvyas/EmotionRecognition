import time

# Start Time
start_time = time.time()



from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import os



haarcascade_path = os.path.join("haarcascade","alt.xml")
model_path = os.path.join("model","emotional_fool.h5")

face_classifier = cv2.CascadeClassifier(haarcascade_path)
classifier =load_model(model_path)


class_labels = ['Angry','Happy','Neutral','Sad','Surprise'] # Remember to keep in alphabetical order

cap = cv2.VideoCapture("data/video/video1.mp4")


# for saving
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# output file name, fourcc code, frame/sec, size tuple
out = cv2.VideoWriter(os.path.join("data","outputvideos","project_haarcascade.avi"), fourcc, 30, (1280,720))



while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    labels = []
        
    if ret == True:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
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
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            
            else:
                cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    else:
        print("Input Video Error. Please check the input source.")
        break
   
    out.write(frame)
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("--- %s seconds ---" % (time.time() - start_time))
























