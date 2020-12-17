<h4>Futurenet Technologies - FR Paper Monitoring Application</h4>

**Decided Architecture Model:** Running FR app in individual VMs. 

**Clarifications:** 

1. _Centralized deployed authentication server:_

   Possible Requirement: When the user logs in to the VM, the login ID and pwd is sent to the server, which authenticates it and sends back the USERID in an encrypted token using JWT (JSON Web Token). This will be used to match against the output label of the face detected by the FR model. If it is a match, the user logs into the paper eval app. 

2. _Webcam access:_

   Possible Requirement: FR application runs inside the VM, access to webcam will be taken care of by VMware Horizon (**Vmware Blast protocol or PCoIP to access local desktop’s camera and microphone from the VM.)** Is there an equivalent in the architecture that is currently set up? 

3. _FR model and face encodings:_

   At present, the python script reads a folder of known faces, extracts the face encodings + face names from them, and stores them in a list/ dictionary. In the VM server-client based setup that we are aiming for, it is not advisable to store the database of known images in each VM. 

   As opposed to images, we note that it is will not be useful to store the known face encodings + names in each VM either. This is because the list of known face encodings + names will have to be updated when a new face is registered. If each VM has an individual copy, this update would be unnecessarily difficult. 

   One possible solution would be using the server/ another VM to send the known face encodings + face names to the client VMs when they bootup. This VM/ server will also be responsible for registering new faces, i.e. extract the encodings from new face and store them with the new name. Each client VM will simply request/ be sent the latest set of face encodings + names from the server during bootup and before the FR app starts. This way we eliminate any local copies of images or face encodings in each VM. 

4. _Running Python script as a service:_ 

   Below is the error that Pranav encountered when he tried to run the basic FR application as a service. 

​     ![service_error](https://github.com/smcck222/futurenetFR/tree/main/notes/service_error.png)

