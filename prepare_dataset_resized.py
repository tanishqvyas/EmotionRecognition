import cv2
import os


emotions = ["Angry", "Sad", "Happy", "Surprise", "Neutral"]


data_save_dir = "/home/tanishq/MAVIS/Intel technovation/EmotionRecognition/data/train"


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

count = 0

for emotion in emotions:

	save_dir = os.path.join(data_save_dir, emotion)

	img_list = load_images_from_folder(emotion)

	print("Starting Folder : ", emotion)
	print()

	for image in img_list:
		count += 1
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray = cv2.resize(gray,(48,48),interpolation=cv2.INTER_AREA)
		cv2.imwrite(os.path.join(save_dir, str(count)+ ".jpg") ,gray)

