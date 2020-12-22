**REFERENCES:** 

1. - [dlib installation Linux](https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/)
   - [dlib installation Windows](https://medium.com/analytics-vidhya/how-to-install-dlib-library-for-python-in-windows-10-57348ba1117f)
   
2. Liveness Detection : 

  - [As a binary classification problem](https://www.pyimagesearch.com/2019/03/11/liveness-detection-with-opencv/)
  - [Blink based liveness detection](https://towardsdatascience.com/real-time-face-liveness-detection-with-python-keras-and-opencv-c35dc70dafd3)
    
    A CNN was trained to classify if an eye was open or close. LeNEt-5 was trained on _Closed Eyes in the Wild (CEW)_ dataset. 
    It is composed of around 4800 eye images in size 24x24. The model gave a 94% accuracy.
    So when an eye is detected, we predict its status using the model, and keep track of the history of its status. The pattern closed-open-closed (1-0-1) indicates a blink, which in turn indicates liveness.
    
  - [Blink detection](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)

3. [Face Recognition](https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/)

4. Making sure all dependencies are installed in the VM. 

   - cmake (including change PATH env variable)
   - dlib 
   - visual studio 2017 was installed 
     -  Need to find an alternative, install a source version of dlib wheel witout the cmake dependency? 
   - Liveness detection will need tensorflow, keras, for the eye and blink detection parts. 

5. Fixes: 
   [Webcam release error cv2](https://stackoverflow.com/questions/53888878/cv2-warn0-terminating-async-callback-when-attempting-to-take-a-picture)
   
6. Sending image across to server
   - https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
   - https://stackoverflow.com/questions/8313374/convert-image-to-json
   - https://stackoverflow.com/questions/19439961/python-requests-post-json-and-file-in-single-request
  
  ```
   def alert_dashboard(frame, alert_type): 
   # Sends alert if unknown to central dashboard.   
    
    cv2.imwrite(filename='intruder_frame.jpg', img=frame)  # Saves intruder frame to same folder.
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    """
    img = Image.fromarray(frame.astype("uint8"))
    img = img.resize((128,128))
    rawBytes = BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    jstr = rawBytes.getvalue()
    """
    print("ALERT TO DASHBOARD" + alert_type + ":" + current_time + ":" + login)
    
    #y = json.dumps(jstr)
    #print(y)   # Prints JSON output to console. 
    
    # TODO: Send JSON output to dashboard.  
    
    #r = requests.post('http://127.0.0.1:5000/dashboard', json = x ) 

    #files = {'media': open('C:/Users/Server/Desktop/futurenetFR/intruder_frame.jpg', 'rb')}
    #requests.post('http://127.0.0.1:5000/dashboard', json = x , files=files)
     
    url = 'http://127.0.0.1:5000/dashboard'
    x = {
        "login_name": login,
        "time": current_time,  
        "type": alert_type,
        "image": "base64 img"
    }

    files = {'filedata': open("C:/Users/Server/Desktop/futurenetFR/intruder_frame.jpg", 'rb')}
    r = requests.post(url, json = x)
    print("[LOG]: Intruder detected -> Alert sent to dashboard")
    ```

