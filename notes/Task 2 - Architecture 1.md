

<h3>ARCHITECTURE 1 - FR APPLICATION RUNNING ON EACH VM</h3>

**Stuff to Clarify:** 

- Ask about the paper eval application and it's requirements, are we building it, how are the papers distributed among professors, should we care about this rn. 
- Pranav - ask sir about CUDA toolkit, Google colab is fine right? 
- VMware horizon? Is that what you mean, will it work out for us and can we avail it through the company. 
- Why did he mention LAN? Do we even need VMware Horizon, or do we need workstation, what does the university want? 

**IDEAS FOR PROCESS FLOW** 

VM (accessed through browser) -  The application runs on bootup (tkinter application maybe) [OR] there will be a personalized environment with files etc.  This can be configured with VMware Horizon. (add details about what it is and how its helpful for us, as we specifically want to access through the browser and not give VM images to each user for them to set up)

There is a centralized deployed authentication server.

The user enters login and password, it to sent to the server. 

Server sends back encrypted token using JWT (JSON Web Token) with the USERID etc. 

In the background, the VM will download the latest FR model from server on bootup, this happens every time the VM is opened through the browser and the application is started. (This solves the problem of re-baking the VMs every time the model is re-trained because of new users (which is a cumbersome and inefficient task)

FR application runs inside the VM, access to webcam will be taken care of my VMware Horizon (**Vmware Blast protocol or PCoIP to access local desktop’s camera and microphone from the VM.**), and the downloaded model will be used to find out whether the face in the webcam matches any of the registered faces. 

If not, an alert is sent to the dashboard (optionally along with a frame from the webcam). 

- This is repeated every 5 minutes. 
- Since the VM is doing less overall, it's allocated resources are idle, and can be used effectively for the FR application, even with future enhanced modifications or higher frequency of checking (every 1 minute) etc. 

**PROS:**

- Downloading the model at bootup removes the issues of re-baking VMs every time the model needs to be retrained. 
- There is scope for modification, increased frequency of checking, and better performance of the FR app because it is running on majorly idle VMs. Better resource utilization. 
- The server load reduces. Now it is used only for authentication, serving the Paper Evaluation application (not enough details about this yet but should be simple). 
- For relatively small number of users [OR] for prototype development, localized FR app would be perfect because scalability is not a major or immediate requirement. 

**CONS**

- Webcam picture quality, bandwidth dependent (still better than sending it across to the server for a centralized FR app)
- Lighting issues 
- It is not scalable. Although cloning is straightforward because the FR model is downloaded on bootup, costs will increase as the number of VMs grow. 
- Since the VM us being used only for limited applications, for a limited period of time (only for the paper evaluation), it might be a waste of resources. 

**Point to remember** : 

- _They could cheat on signup, by signing up with the picture of the research scholar?_

  The solution will depend on how we obtain images for training our FR model. Is it going to be trained on Webcam images? (We'll need around 100 images per person). Should we leave it to the university to take care of this and provide us with the right pictures for training/ signup? Should we retrain the model as usual and then cross verify with a university DB of images? But if it doesn't match, we'll have to rollback to the previous model, so how to accomplish that on the server side? 

- _Could use a picture of the professor at an appropriate distance from the device_. 

- _Does this type of distributed FR app in each VM decrease security and how?_ 

  [Link to relevant paper](http://www.iraj.in/journal/journal_file/journal_pdf/12-161-143617620637-39.pdf)

- Are there any additional system requirements that we would require because the model is distributed FR as compared to centralized (where the client is not doing much) and how much will this affect cost during scaling? 

**ORGANIZATION FOR PPT: **

- First slide - heading 

- Intro (About the Localized FR architecture)

- Centralized  VS Distributed FR App. 

- Advantages 

- Disadvantages 

- Frameworks identified  (and what we will require from Futurenet) 

  VMware Horizon 

  Centralized deployed authentication server. 

  Training DL Model (On Colab, GPU, TPU is there, I don't think we'll need more) 

  FR App 

  Dashboard - Rest API? 

  Paper Evaluation App - Rest API? 

  Authentication 

- General problems wrt FR test cases, and disadvantages of using VMs in the first place. 





