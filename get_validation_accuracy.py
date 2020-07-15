import time

# Start Time
start_time = time.time()



from tensorflow.keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import os
from mtcnn import MTCNN



num_classes = 5  # we have 5 kinds of emotions
img_rows, img_cols = 48, 48

# Dataset Path
test_data_dir = os.path.join("data","validation")
# test_data_dir = os.path.join("Flickr","yo")


model_name = input("\n\nEnter the model name : ")
model_name = model_name + '.h5'

print("-------------------Loading the model------------------------------")
model_path = os.path.join("model",model_name)
classifier = load_model(model_path)
print("-------------------Model Loaded Succesfully------------------------------")


class_labels = ['Angry','Happy','Neutral','Sad','Surprise'] # Remember to keep in alphabetical order

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

# Count array to keep track of all correct predictions
count = [0 for i in range(num_classes)]

# Total count array
tot_count = [0 for i in range(num_classes)]

for emotion in range(num_classes):

	print("The current emotion is : ", class_labels[emotion])

	# Getting the images
	path = os.path.join("data","validation", class_labels[emotion])
	image_list = load_images_from_folder(path)

	# Setting the total count and initial count
	tot_count[emotion] = len(image_list)
	correct_pred = 0

	for img in image_list:


		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		roi_gray = cv2.resize(gray,(48,48),interpolation=cv2.INTER_AREA)
		roi = roi_gray.astype('float')/255.0
		roi = img_to_array(roi)
		roi = np.expand_dims(roi,axis=0)


		# Getting the prediction for an image
		cur_prediction = classifier.predict(roi)[0]
		cur_prediction = class_labels[list(cur_prediction).index(max(cur_prediction))]

		# print("Current Prediction : ", cur_prediction )
		# print("True Prediction : ", class_labels[emotion])

		# if(class_labels[emotion] != 'Sad'):
		if(cur_prediction == class_labels[emotion]):
			count[emotion] += 1

		# else:
		# 	if(cur_prediction == class_labels[emotion] or cur_prediction == 'Neutral'):
		# 		count[emotion] += 1



print("\Validation Summary for the model : ", model_name)
for i in range(num_classes):

	print(class_labels[i], " : ", (count[i]/tot_count[i])*100)

print("\nTotal Accuracy on validation set is: ")
print((sum(count)/sum(tot_count))*100)
