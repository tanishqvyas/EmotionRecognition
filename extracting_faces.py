from mtcnn import MTCNN
import cv2
# img = cv2.imread('Flickr/yo/Angry/anger_0000.jpg')
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

path = os.path.join("Flickr","yo", class_labels[emotion])
image_list = load_images_from_folder(path)

def extract_image(img,count):
    detector = MTCNN()
    faces = detector.detect_faces(img)
    for f in faces:
        x,y,w,h = f.get('box')
        # Rect = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # img = Rect
        ROI = img[y:y+h, x:x+w]
        roi_resized = cv2.resize(ROI,(48,48),interpolation=cv2.INTER_AREA)
        # only_face = cv2.cvtColor(ROI,cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(roi_resized,cv2.COLOR_BGR2GRAY)
        cv2.imwrite(str(count)+'.jpg',gray)
        print("kiya",count)

for i in range(len(image_list)):
    extract_image(image_list[i],i)
    