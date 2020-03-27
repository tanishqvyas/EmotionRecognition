from mtcnn import MTCNN
import cv2
img = cv2.imread('img.jpg')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
detector = MTCNN()
faces = detector.detect_faces(img)
for f in faces:
    x,y,w,h = f.get('box')
    Rect = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
    img = Rect
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    cv2.imwrite('detect.jpg',img)
