import urllib.request

#check if connected to the internet
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
if connect() == False:
    print('Not connected to the internet!!!')
    print('Exiting application.....')
    exit()

#intervel to take the next video
WAIT_PERIOD = 25

#modules needed
import cv2
import numpy as np
from drive_functions import *
import time
import os
import threading
import keyboard

print('Url from where the video is captured..')
#read the info file
with open('info','r+') as url_info:
    u,p,url = url_info.readlines()
    u_no = int(u[0])
    p_no = int(p[0])
    url = url[0:7]+u[1:1+u_no]+':'+p[1:1+p_no]+'@'+url[7:]

print(url)

#trying to access video
try:
    cap = cv2.VideoCapture(url)
except:
    pass

if cap.isOpened() != True:
    print('No video found')
    exit()

i=0
#using .avi less space
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
w = int(cap.get(3))
h = int(cap.get(4))
fps = int(cap.get(5))

#folder for storing data
os.system('mkdir data')

#for drive folder
vid_id = check_folder_exists('data',0)
if vid_id == False:
    vid_id = create_folder('data')
else:
    print('A previous instance of Data exists!!\nDelete it y/n?')
    opt = input()
    if opt == 'y' or 'Y':
        vid_id = drive.CreateFile({"id":vid_id})
        vid_id.Delete()
        vid_id = create_folder('data')

#log of files done
log = open('log.txt','w+')
vid_ids = open('vid_ids.txt','w+')

#initialise timer
start = time.time()
files_counter = 0

while(not keyboard.is_pressed('q')):
    ret,frame = cap.read()
    if(int(time.time()-start)%WAIT_PERIOD == 0):
        i+=1
        out = cv2.VideoWriter('data//'+str(i)+'.avi', fourcc, fps, (w,h),0)
        for j in range(105):
            ret,frame = cap.read()
            if ret == True:
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                out.write(gray)
        out.release()
        log.write(str(i)+'.avi is successfully captured and saved\n')
        vid_ids.write('\n'+str(i)+'.avi: ')
        t1 = threading.Thread(target=upload_file_save_id, args=(vid_ids,str(i)+'.avi',str(i)+'.avi','data',vid_id))
        t1.start()
        log.write(str(i)+'.avi is successfully uploaded\n\n')
        inst = drive.CreateFile({"title":str(i)})
        inst.Upload()
        files_counter += 1

#end any uploading tasks
t1.join()
print(time.time()-start)
cap.release()
log.close()
upload_file('log.txt','log.txt')
print()
print(f"A total of {files_counter} videos were captured and sent in the present session")
print()
vid_ids.close()
cv2.destroyAllWindows()
