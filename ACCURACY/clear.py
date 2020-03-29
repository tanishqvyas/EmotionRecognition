import os

emotions = ["Angry","Happy","Neutral","Sad","Surprise"]

for emt in emotions:
    os.chdir(emt)
    for emt in emotions:
        try:
            os.system("del "+emt+"* 2> 2")
            os.system("del 2")
        except :
            pass
    os.chdir("..")
