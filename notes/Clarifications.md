<h4>Futurenet Technologies - FR Paper Monitoring Application</h4>

**Decided Architecture Model:** Running FR app in individual VMs. 

**Clarifications:** 

1. Centralized deployed authentication server:

   Possible Requirement: When the user logs in to the VM, the login ID and pwd is sent to the server, which authenticates it and sends back the USERID in an encrypted token using JWT (JSON Web Token). This will be used to match against the output label of the face detected by the FR model. If it is a match, the user logs into the paper eval app. 

2. Webcam access: 

   Possible Requirement: FR application runs inside the VM, access to webcam will be taken care of by VMware Horizon (**Vmware Blast protocol or PCoIP to access local desktop’s camera and microphone from the VM.** Is there an equivalent in the architecture that is currently set up? 

3. FR model: 

   If the VMs are deployed with the FR model inside them, every time we retrain the model as new faces are registered, we would have to re-bake new VM images with the new model, to replace the old VMs. A better solution is to keep the VMs as they are, with only the paper eval app, and instead download the FR model from the server on bootup of the VM. Once the model is downloaded, the FR app starts running in the background. 

   

   

