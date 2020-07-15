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

#email address of the client
CLIENT_ID = 'rajathjnxcopy@gmail.com'

#modules needed
import time
import os
import threading
import keyboard
from drive_functions import *
from face_emot_detect import *
from send_email import send_email

os.system('cls')

start = time.time()
log_info = search_download('log.txt')
if log_info:
    print('Log file found ')
    print('both client and server not running at same time!!')
    log = drive.CreateFile({"id":log_info})
    log.Delete()
    with open('log.txt','r') as l:
        log_info = int(len(l.readlines())/3)
    os.remove('log.txt')
else:
    print('Client and server are running at realtime.')
    print('Note: If any error occurs it probably means the that the client is malfunctioning')

results = open('result.txt','w+')
os.system('mkdir results')

#for drive
resID = check_folder_exists('results',0)
if resID == False:
    resID = create_folder('results')
else:
    print('A previous instance of results exists!!\nDelete it y/n?')
    opt = input()
    if opt == 'y' or 'Y':
        res = drive.CreateFile({"id":resID})
        res.Delete()
        resID = create_folder('results')

#if log file is present it means that the client and server are not running in realtime
if log_info:
    dataID = check_folder_exists('data',0)
    if dataID == False:
        print('Log file there and data folder not found??')
        print('Please check once again')
        exit()
    d1 = threading.Thread(target=download_file,args=(dataID,False,True))
    d1.start()
    d1.join()
    for video in range(1,log_info+1):
        video = str(video)+'.avi'
        print(video)
        emotions = face_emot_detect('data//'+video, video, 'results')
        print(f'result of {video}: emotions found and its weight {emotions}')
        results.write(f'result of {video}: and emotions found and its weight {emotions} \n')
        t1 = threading.Thread(target=upload_file_save_id,args=(results,video,video,'results',resID))
        t1.start()
    t1.join()
    results.close()
    send_email(CLIENT_ID,
                'Results of the image detection',
                'The result file is attached',
                'result.txt')
    print(time.time()-start)
    exit()
else:
    while(True):
        dataID = check_folder_exists('data',0)
        if dataID == False:
            print('Searching for Data folder ...')
            time.sleep(1)
        else:
            print('Data folder found !!')
            break
    error = 0
    vid_inst = 1
    os.system('mkdir data')
    while(not keyboard.is_pressed('q')):
        os.chdir('data')
        #search for upload video number
        num = search_download(str(vid_inst))
        if num == False:
            #find video until available
            while(True):
                print(vid_inst)
                time.sleep(1)
                num = search_download(str(vid_inst))
                if num != False:
                    break
                if keyboard.is_pressed('q'):
                    results.close()
                    os.chdir('..')
                    send_email(CLIENT_ID,
                        'Results of the image detection',
                        'The result file is attached',
                        'result.txt')
                    print(time.time()-start)
                    print("Do you want to clean up the data folder")
                    choice = input("y/n??")
                    if(choice == "y"):
                        os.remove("data")
                    print("Do you want to clean up the results")
                    choice = input("y/n??")
                    if(choice == "y"):     
                        os.remove("result.txt")
                        os.remove("*.avi")
                    exit()
                    exit()
                
        #If file found remove its log and download it
        inst = drive.CreateFile({"id":num})
        inst.Delete()
        os.remove(str(vid_inst))
        search_download(str(vid_inst)+'.avi',dataID)
        os.chdir('..')
        video = str(vid_inst)+'.avi'
        print(video)
        emotions = face_emot_detect('data//'+video, video, 'results')
        if emotions == False:
            error +=1
        print(f'result of {video}: emotions found and its weight {emotions}')
        results.write(f'result of {video}: and emotions found and its weight {emotions} \n')
        try:
            opt = upload_file_save_id(results,video,video,'results',resID)
            if opt==False:
                error+=1
        except:
            error += 1
        if error >= 3:
            send_email(CLIENT_ID,
                'Error in client',
                'Videos from client are not being detected. The client is malfuncting',
                'result.txt')
            error = 0
        if emotions != False:
            if sum(list(emotions.values())) >= 20:
                send_email(CLIENT_ID,
                    f'Result of {video}',
                    f'result of {video}: emotions found and its weight {emotions}'
                )
        vid_inst += 1
    results.close()
    send_email(CLIENT_ID,
                'Results of the image detection',
                'The result file is attached',
                'result.txt')
    print(time.time()-start)
    exit()

print()
print()
print("Do you want to clean up the data folder")
choice = input("y/n??")
if(choice == "y"):
    os.remove("data")
print("Do you want to clean up the results")
choice = input("y/n??")
if(choice == "y"):
    os.remove("*.avi")
    os.remove("result.txt")
