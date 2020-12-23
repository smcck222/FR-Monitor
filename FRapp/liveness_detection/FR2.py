import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # To supress TensorFlow messages. 
import warnings # To supress warnings. 
import cv2
import face_recognition
from PIL import Image
import numpy as np
import tqdm as tqdm
from imutils.video import VideoStream
from collections import defaultdict
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import time 
from datetime import datetime
import json
import base64
from PIL import Image 
from io import BytesIO
import requests

IMG_SIZE = 24 
start_time = 0 
login = "sherin"
first_alive = False

def load_model():

	json_file = open('C:/Users/Server/Desktop/futurenetFR/models/model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("C:/Users/Server/Desktop/futurenetFR/models/model.h5")
	loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return loaded_model

def predict(img, model):
	
	img = Image.fromarray(img, 'RGB').convert('L')
	img = imresize(img, (IMG_SIZE,IMG_SIZE)).astype('float32')
	img /= 255
	img = img.reshape(1,IMG_SIZE,IMG_SIZE,1)
	prediction = model.predict(img)
	if prediction < 0.1:
		prediction = 'closed'
	elif prediction > 0.9:
		prediction = 'open'
	else:
		prediction = 'idk'
	return prediction

def init():

	face_cascPath = 'C:/Users/Server/Desktop/futurenetFR/models/haarcascade_frontalface_alt.xml'
	open_eye_cascPath = 'C:/Users/Server/Desktop/futurenetFR/models/haarcascade_eye_tree_eyeglasses.xml'
	left_eye_cascPath = 'C:/Users/Server/Desktop/futurenetFR/models/haarcascade_lefteye_2splits.xml'
	right_eye_cascPath ='C:/Users/Server/Desktop/futurenetFR/models/haarcascade_righteye_2splits.xml'
	face_detector = cv2.CascadeClassifier(face_cascPath)
	open_eyes_detector = cv2.CascadeClassifier(open_eye_cascPath)
	left_eye_detector = cv2.CascadeClassifier(left_eye_cascPath)
	right_eye_detector = cv2.CascadeClassifier(right_eye_cascPath)

    # To open webcam. 
	video_capture = VideoStream(src=0).start()
	
	model = load_model()
	return (model,face_detector, open_eyes_detector, left_eye_detector,right_eye_detector, video_capture) 

def encode_known_faces(folder_path):
    # initialize the list of known encodings and known names
    known_encodings = []
    known_names = []

    for filename in os.listdir(folder_path):
        input_image = face_recognition.load_image_file(os.path.join(folder_path, filename))
        
        image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
     
        # detect face in the image and get its location (square boxes coordinates)
        boxes = face_recognition.face_locations(image, model='hog')

        # Encode the face into a 128-d embeddings vector
        encoding = face_recognition.face_encodings(image, boxes)

        # the person's name is the name of the folder where the image comes from
        name = filename[:-5]

        if len(encoding) > 0 : 
            known_encodings.append(encoding[0])
            known_names.append(name)

    return {"encodings": known_encodings, "names": known_names}

def isBlinking(history, maxFrames):
    """ @history: A string containing the history of eyes status 
         where a '1' means that the eyes were closed and '0' open.
        @maxFrames: The maximal number of successive frames where an eye is closed """
    for i in range(maxFrames):
        pattern = '1' + '0'*(i+1) + '1'
        if pattern in history:
            return True
    return False

def display_result(frame): 
    
    cv2.imshow("Face Liveness Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            return("exit")

def alert_dashboard(frame, alert_type): 
# Sends alert if unknown to central dashboard.   
    
    cv2.imwrite(filename='intruder_frame.jpg', img=frame)  # Saves intruder frame to same folder.
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    image = "base64 img"  # TODO: Figure out how to send this.
    url = 'http://127.0.0.1:5000/dashboard'
    x = {
        "login_name": login,
        "time": current_time,  
        "type": alert_type,
        "image": image
    }

    # Sending alert as JSON object to dashboard. 
    r = requests.post(url, json = x)   
    print("[LOG]: Intruder detected -> Alert sent to dashboard")


def fr_monitor(model, video_capture, face_detector, open_eyes_detector, left_eye_detector, right_eye_detector, data):
    
    global start_time
    global first_alive
    eyes_detected = defaultdict(str)
    while True: 
        frame = video_capture.read()
        # Process the frame.
        frame = cv2.resize(frame, (0, 0), fx=0.6, fy=0.6)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # for each detected face
        for (x,y,w,h) in faces:
            # Encode the face into a 128-d embeddings vector
            encoding = face_recognition.face_encodings(rgb, [(y, x+w, y+h, x)])[0]

            # Compare the vector with all known faces encodings
            matches = face_recognition.compare_faces(data["encodings"], encoding)

            # Before recognition.
            name = "unknown face"

            # If there is at least one match:
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number of votes
                name = max(counts, key=counts.get)

            face = frame[y:y+h,x:x+w]
            gray_face = gray[y:y+h,x:x+w]

            eyes = []
            
            # Eyes detection
            # check first if eyes are open (with glasses taking into account)
            open_eyes_glasses = open_eyes_detector.detectMultiScale(
                gray_face,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
            )
            # if open_eyes_glasses detect eyes then they are open 
            if len(open_eyes_glasses) == 2:
                eyes_detected[name]+='1'
                for (ex,ey,ew,eh) in open_eyes_glasses:
                    cv2.rectangle(face,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
            # otherwise try detecting eyes using left and right_eye_detector
            # which can detect open and closed eyes                
            else:
                # separate the face into left and right sides
                left_face = frame[y:y+h, x+int(w/2):x+w]
                left_face_gray = gray[y:y+h, x+int(w/2):x+w]

                right_face = frame[y:y+h, x:x+int(w/2)]
                right_face_gray = gray[y:y+h, x:x+int(w/2)]

                # Detect the left eye
                left_eye = left_eye_detector.detectMultiScale(
                    left_face_gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags = cv2.CASCADE_SCALE_IMAGE
                )

                # Detect the right eye
                right_eye = right_eye_detector.detectMultiScale(
                    right_face_gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags = cv2.CASCADE_SCALE_IMAGE
                )

                eye_status = '1' # we suppose the eyes are open

                # For each eye check wether the eye is closed.
                # If one is closed we conclude the eyes are closed
                for (ex,ey,ew,eh) in right_eye:
                    color = (0,255,0)
                    pred = predict(right_face[ey:ey+eh,ex:ex+ew],model)
                    if pred == 'closed':
                        eye_status='0'
                        color = (0,0,255)
                    cv2.rectangle(right_face,(ex,ey),(ex+ew,ey+eh),color,2)
                for (ex,ey,ew,eh) in left_eye:
                    color = (0,255,0)
                    pred = predict(left_face[ey:ey+eh,ex:ex+ew],model)
                    if pred == 'closed':
                        eye_status='0'
                        color = (0,0,255)
                    cv2.rectangle(left_face,(ex,ey),(ex+ew,ey+eh),color,2)
                eyes_detected[name] += eye_status

            if name == "unknown face":
                # ALERT the dashboard about unknown face. 
                alert_dashboard(frame, name)

            else: 
                # Each time, we check if the person has blinked
                # If yes, we display its name
                if isBlinking(eyes_detected[name],3):
                    
                    first_alive = True
                    start_time = time.perf_counter()
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    # Display name
                    y = y - 15 if y - 15 > 15 else y + 15
                    cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
                    
                    eyes_detected[name] = ''
                
                else: 
                    
                    if first_alive == False: 
                        wait_time = 300
                    else:
                        wait_time = 15

                    time_since_last_blink = time.perf_counter() - start_time 
                    if time_since_last_blink > wait_time: 
                        # ALERT the dashboard about no blinking => no liveness
                        
                        alert_dashboard(frame, "no_blink") 
                        
        # If required, to check output on video. 
        if display_result(frame) == "exit": 
            break

def main(): 
    
    warnings.filterwarnings('ignore')  # To supress warnings.

    print("[LOG]: Encoding Faces")
    # Change this to appropriate folder.
    data = encode_known_faces("C:/Users/Server/Desktop/futurenetFR/known_faces")
    print("[LOG]: Encoded Known Faces") 

    # Load Face and Eye models. 
    (model, face_detector, open_eyes_detector,left_eye_detector,right_eye_detector, video_capture) = init()
    
    start_time = time.perf_counter()
    print("[LOG]: Starting FR Monitor") 
    fr_monitor(model, video_capture, face_detector, open_eyes_detector,left_eye_detector,right_eye_detector, data)
       
    cv2.destroyAllWindows()
    video_capture.stop()

if __name__ == "__main__":
    main() 
