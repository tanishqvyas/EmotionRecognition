**Folder structure**

```
+
|--- data
|	|
|	|--- outputvideos
|	|
|	|--- video
|	|	|
|	|	|--- video.mp4
|	|	|--- video1.mp4
|	|
|	|--- train
|	|	|
|	|	|--- Angry
|	|	|--- Happy
|	|	|--- Neutral
|	|	|--- Sad
|	|	|--- Surprise
|	|	
|	|--- validation
|	|	|
|	|	|--- Angry
|	|	|--- Happy
|	|	|--- Neutral
|	|	|--- Sad
|	|	|--- Surprise
|	|	
|	|--- test
|	|	|
|	|	|--- Angry
|	|	|--- Happy
|	|	|--- Neutral
|	|	|--- Sad
|	|	|--- Surprise
|
|--- haarcascade
|	|
|	|--- alt.xml
|	|--- final.xml
|
|
|--- model
|	|
|	|--- EluEmotional.h5
|	|--- emotional_fool.h5
|	|--- Emotion_little_vgg.h5
|	|--- ReluEmotional.h5
|
|
|--- emotion_detect_video_haarcascade.py
|--- emotion_detect_video_mtcnn.py
|--- face_detect_image.py
|--- face_detect_video.py
|--- prepare_dataset_resized.py
|--- train_model.py
|--- get_testing_accuracy.py
|--- README.md
|
+

```