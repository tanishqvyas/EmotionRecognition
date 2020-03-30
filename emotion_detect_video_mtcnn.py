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
from mtcnn import MTCNN




# Importing the MTCNN detector to detect faces
detector = MTCNN()

# Path to the emotion detection model
model_path = os.path.join("model","EluEmotional.h5")
classifier =load_model(model_path)

class_labels = ['Angry','Happy','Neutral','Sad','Surprise'] # Remember to keep in alphabetical order



# for saving
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# output file name, fourcc code, frame/sec, size tuple
out = cv2.VideoWriter(os.path.join("data","outputvideos","project_mtcnn.avi"), fourcc, 30, (1280,720))


"""
Taking video input

1. Live Feed
cap = cv2.VideoCapture(0)

2. Recorded Video
cap = cv2.VideoCapture('path/to/video/file')

"""
cap = cv2.VideoCapture("data/video/video1.mp4")
# cap = cv2.VideoCapture(0)

while(True):

    # Read one frame at a time
    ret, frame = cap.read()
    labels = []

    # If a frame is returned
    if ret == True:
        
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # Get a dictionary of all faces
        faces = detector.detect_faces(frame)

        # For every face in the faces detected in the current frame
        for face in faces:            

            # Get the confidence value of the 'f' being a face
            if face.get('confidence')>=0.9:

                # Get the co-ordinates of the cropped area wherein face lies
                x,y,w,h = face.get('box')

                # Draw a Rectangle
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)

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


        out.write(frame)
        cv2.imshow("My Image WIndow", frame)

        # If q is pressed then quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # If no frame is read in
    else:
        print("Input Video Error. Please check the input source.")
        break

# Freeing all resources
out.release()
cap.release()
cv2.destroyAllWindows()

print("--- %s seconds ---" % (time.time() - start_time))