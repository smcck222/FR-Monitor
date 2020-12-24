<h5>FUTURENET TECHNOLOGIES (INDIA) PVT LIMITED<br>Face Recognition Based Monitoring Application for Paper Evaluation</h5>

**OVERVIEW:** 

This application's user base is government medical colleges that require a monitoring system for remote paper evaluation. Each user is provided with a VM that is accessed through the browser and the FR app runs on bootup. The webcam is accessed and when an unknown face appears in the frame, an alert is sent to the central dashboard. 

**REQUIREMENTS/ INSTALLATIONS:** 

- Python (3.7.3 on my system)

- Libraries (to install)

  - OpenCV 

    _pip install opencv-python_

  - face-recognition (cmake, dlib)
    
    _pip install cmake_ 
                        
    _pip install dlib_  
    
    Use admin cmd only

  - requests 

    _pip install requests_

In addition, 

- _pip install flask_ for the flask server. 

**COMPONENTS:**

- Known Faces Database: 

  A database of known faces/ users is maintained. With 10 images per person. 

- Modules 

  1. _encode_known_faces_: 

     Face encodings and face names are extracted from a folder of known faces. 

  2. _display_result_: 

     Displays the frame with a box around the recognized face and its label (unknown/ name) 

  3. _check_alert_dashboard:_ 

     Saves the frame captured when the intruder is on the screen. Sends timestamp, login name, and image to the central dashboard. 

  4. _fr_monitor:_ 

     Monitors for unknown faces in a looped manner, exits when an intruder is found. 

     Finds all faces in the frame and extracts their face encodings. Compares the extracted encodings with the known encodings and hence finds the label/ name. 

     Vote-based approach - The extracted encodings are compared with the entire set of known encodings. The name/ label that matches the largest number of times is determined as the recognized face. This reduces chances of error in the face recognition. 

     **_process_this_frame_** is a variable that is toggled inside the loop such that every other frame is processed. 

     The loop is exited if an intruder's face is recognized. 

**TROUBLESHOOTING:**

- Installation issues for **face_recognition** 

  References: 

  - link1
  - link2
