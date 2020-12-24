**OBJECTIVE:** 

App to check for unknown faces in the webcam frame in order to assist paper evaluation monitoring. Alerts are sent to central React Dashboard running on a Spring server, with a MySQL database in the backend. 

**DESCRIPTION:** 

- _basic_fr_ : Basic FR monitoring, without liveness detection. 
- _live_detection_ : Blink-based liveness detection added to FR. 
- _known_faces_ : Database of known registered faces. 
  
  Adding more registered faces: 
  - Add 6 pictures of face, named appropriately i.e. newfacename1.jpg, newfacename2.jpg, etc. 
- _flask_server.py_ : Flask server to recieve the alerts from the FR app. For testing purposes. 

**REFERENCES:** 

1. - [dlib installation Linux](https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/)
   - [dlib installation Windows](https://medium.com/analytics-vidhya/how-to-install-dlib-library-for-python-in-windows-10-57348ba1117f)
   
2. Liveness Detection : 

  - [As a binary classification problem](https://www.pyimagesearch.com/2019/03/11/liveness-detection-with-opencv/)
  - [Blink based liveness detection](https://towardsdatascience.com/real-time-face-liveness-detection-with-python-keras-and-opencv-c35dc70dafd3)
    
    A CNN was trained to classify if an eye was open or close. LeNEt-5 was trained on _Closed Eyes in the Wild (CEW)_ dataset. 
    It is composed of around 4800 eye images in size 24x24. The model gave a 94% accuracy.
    So when an eye is detected, we predict its status using the model, and keep track of the history of its status. The pattern closed-open-closed (1-0-1) indicates a blink,  which in turn indicates liveness.
    
  - [Blink detection](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)

3. [Face Recognition](https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/)

**FIXES:** 

1. [Webcam release error cv2](https://stackoverflow.com/questions/53888878/cv2-warn0-terminating-async-callback-when-attempting-to-take-a-picture)
   
2. How to send images accross to the server and receive them on the server side? 

   - https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
   - https://stackoverflow.com/questions/8313374/convert-image-to-json
   - https://stackoverflow.com/questions/19439961/python-requests-post-json-and-file-in-single-request


#ATTEMPT1

```
   def alert_dashboard(frame, alert_type): 
   # Sends alert if unknown to central dashboard.   
    
    cv2.imwrite(filename='intruder_frame.jpg', img=frame)  # Saves intruder frame to same folder.
   
    img = Image.fromarray(frame.astype("uint8"))
    img = img.resize((128,128))
    rawBytes = BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    jstr = rawBytes.getvalue()
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    url = 'http://127.0.0.1:5000/dashboard'
    x = {
        "login_name": login,
        "time": current_time,  
        "type": alert_type,
        "image": jstr
    }

    r = requests.post('http://127.0.0.1:5000/dashboard', json = x ) 
    print("[LOG]: Intruder detected -> Alert sent to dashboard")
 ```
    
#ATTEMPT2
 ```
   def alert_dashboard(frame, alert_type): 
   # Sends alert if unknown to central dashboard.   
   
   cv2.imwrite(filename='intruder_frame.jpg', img=frame)  # Saves intruder frame to same folder.
   now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    url = 'http://127.0.0.1:5000/dashboard'
    x = {
        "login_name": login,
        "time": current_time,  
        "type": alert_type,
        "image": jstr
    }

   
   files = {'media': open('C:/Users/Server/Desktop/futurenetFR/intruder_frame.jpg', 'rb')}

   requests.post('http://127.0.0.1:5000/dashboard', json = x , files=files)
   # requests.post('http://127.0.0.1:5000/dashboard', data = x , files=files)
   
   print("[LOG]: Intruder detected -> Alert sent to dashboard")
```
