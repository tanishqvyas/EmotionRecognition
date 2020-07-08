from mtcnn import MTCNN
import cv2
import os
# img = cv2.imread('Flickr/yo/Angry/anger_0000.jpg')
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

# path = os.path.join("Flickr","yo", class_labels[emotion])
# path = os.path.join("Angry")

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images
image_list = load_images_from_folder("Sad")

def extract_image(img,count):
    detector = MTCNN()
    faces = detector.detect_faces(img)
    ind=0
    for f in faces:
        x,y,w,h = f.get('box')
        # Rect = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # img = Rect
        ROI = img[y:y+h, x:x+w]
        try:
            roi_resized = cv2.resize(ROI,(48,48),interpolation=cv2.INTER_AREA)
            # only_face = cv2.cvtColor(ROI,cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(roi_resized,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(str(i+10000)+'.jpg',gray)
            # print("kiya",count+ind)
            # ind+=1
            # count+=1
            # return count
        except:
            pass
print(len(image_list))
# k=0 
detector = MTCNN()
ind=10000
for i in range(len(image_list)):
    img=image_list[i]
    faces = detector.detect_faces(img)
    for f in faces:
        x,y,w,h = f.get('box')
        # Rect = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # img = Rect
        ROI = img[y:y+h, x:x+w]
        try:
            roi_resized = cv2.resize(ROI,(48,48),interpolation=cv2.INTER_AREA)
            # only_face = cv2.cvtColor(ROI,cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(roi_resized,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(str(ind)+'.jpg',gray)
            print("kiya",ind)
            ind+=1
            # count+=1
            # return count
        except:
            pass
    # extract_image(image_list[i],i)

    