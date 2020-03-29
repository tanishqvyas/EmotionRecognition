import numpy as np
import cv2
import os
import datetime
from datetime import date

os.system("mkdir images")
videos = os.listdir()
count = 0
img=0
for video in videos:
	cap = cv2.VideoCapture(video)
	print(video)
	while(True):
		ret, frame = cap.read()
		ret, frame = cap.read()
		ret, frame = cap.read()
		ret, frame = cap.read()
		ret, frame = cap.read()
		img+=1
		count=img
		if ret ==True:
			img_name = "images\\"+ str(img) +".jpg"
			cv2.imwrite(img_name,frame)
		else:
			break

# cv2.release()
	cap.release()
	print("done")

cv2.destroyAllWindows()
