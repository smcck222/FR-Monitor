import face_recognition
import cv2
import os
import json
from datetime import datetime
import requests

video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
login = "sherin" 
intruder = 0
alert = "unknown face"
known_face_encodings = [] 
known_face_names = [] 

def encode_known_faces(folder_path): 
# Function to load folder of known pictures and store face encodings. 

    for filename in os.listdir(folder_path):
        input_image = face_recognition.load_image_file(os.path.join(folder_path, filename))
        face_encoding = face_recognition.face_encodings(input_image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(filename[:-5])

def display_result(name, frame, face_locations, face_names): #Press 'q' to exit this window.
# Display in video, for testing purposes (actual app runs in background, no video)
    
    for (top, right, bottom, left), name in zip(face_locations, face_names):
           
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size.
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face.
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face.
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return("exit")
    
def check_alert_dashboard(name, frame): 
# Sends alert if unknown to central dashboard.   
    global intruder
    if name==alert and intruder==0:
        
        cv2.imwrite(filename='intruder_frame.jpg', img=frame)  # Saves intruder frame to same folder.
        intruder = 1
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        image = "base64 img"  # TODO: Figure out how to send this.
        alert_type = "unknown face"
        
        url = 'http://127.0.0.1:5000/dashboard'
        x = {# JSON object. 
            
            "login_name": login,
            "time": current_time,  
            "type": alert_type,
            "image": image
        }

        # Sending alert as JSON object to dashboard. 
        r = requests.post(url, json = x)   
        
        #y = json.dumps(x)
        #print(y)   # Prints JSON output to console. 
        
        print("[LOG]: Intruder detected -> Alert sent to dashboard")
        

def fr_monitor(): 
# Monitors for unknown faces. 

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = [] 
    process_this_frame = True
    name = ""
    global logged_in
    
    while True:   # Continuous loop for monitoring.
        
        # Grab a single frame of video. 
        ret, frame = video_capture.read() 

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = [] 
            if not face_encodings:  # No face encodings found in the frame. 
                name = "No Face Found"
            
            else: 
                for face_encoding in face_encodings: 
                    # This loops through all faces found in frame. 
                    name = "unknown face"  # Before Recognition. 

                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    
                    # If there is at least one match:
                    if True in matches:
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}
                        for i in matchedIdxs:
                            name = known_face_names[i]
                            counts[name] = counts.get(name, 0) + 1

                        # Determine the recognized face with the largest number of votes
                        name = max(counts, key=counts.get)
                    
                    face_names.append(name)
                
        process_this_frame = not process_this_frame   # As we are processing every other frame. 
        #print(name)
        
        # Action after FR = display/ send notification. 
        check_alert_dashboard(name, frame)

        # If required, to check output on video.
        #if display_result(name, frame, face_locations, face_names) == "exit": 
        #    break
        
        if intruder == 1: # Exits continuous monitoring loop if unknown face is found.
            break

def main(): 

    # Change this to appropriate folder. 
    known_faces_path = "C:/Users/Server/Desktop/futurenetFR/known_faces"
    encode_known_faces(known_faces_path)
    print("[LOG]:Known faces encoded")
    print("[LOG]:Starting FR Monitor")
    fr_monitor()
    print("[LOG]:Exiting")
    video_capture.release()
    cv2.destroyAllWindows() 

if __name__ == "__main__":
    main()
