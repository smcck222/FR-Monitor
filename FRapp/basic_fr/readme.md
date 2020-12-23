**Features:** 
- Application to monitor for unknown faces in the webcam frame. 
- INPUT: Webcam frame. 
- OUTPUT: Alert sent to dashboard, if unknown face is found. Program terminates once this happens. 
- No liveness detection. 
- To add more faces, check the _known_faces_ folder and update it. 

**To Do:** 
- Change the path of the _known_faces_ folder as required. 
- Change the URL in the function _check_alert_dashboard_ as required, to send the JSON data to the server. 
- Install all requirements as mentioned in _Documentation FR1.md_ 
