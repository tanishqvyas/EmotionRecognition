import cv2

from mtcnn import MTCNN

# Importing the MTCNN detector to detect faces
detector = MTCNN()

# for saving
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# output file name, fourcc code, frame/sec, size tuple
out = cv2.VideoWriter('project.avi', fourcc, 15, (1280,720))


"""
Taking video input

1. Live Feed
cap = cv2.VideoCapture(0)

2. Recorded Video
cap = cv2.VideoCapture('path/to/video/file')

"""
cap = cv2.VideoCapture("data/video/video1.mp4")

while(True):

    # Read one frame at a time
    ret, frame = cap.read()

    # If a frame is returned
    if ret == True:

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

        out.write(frame)
        # cv2.imshow("My Image WIndow", frame)

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