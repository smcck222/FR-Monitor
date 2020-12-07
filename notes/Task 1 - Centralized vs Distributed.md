**CHOOSING THE ARCHITECTURE FOR FR APPLICATION** 

_**Futurenet Technologies**_

GPU: (Device Manager->Display Adapters)
Nvidia Driver Version: (Nvidia Control Panel->System Information->Details)  
Nvidia GeForce MX110, version : 451.67 

_The NVIDIA Driver is the software driver for **NVIDIA Graphics GPU** installed on the PC. It is a program used to communicate from the Windows PC OS to the device. This software is required in most cases for the hardware device to function properly._

[What's the Difference Between a CPU vs a GPU? | NVIDIA Blog](https://blogs.nvidia.com/blog/2009/12/16/whats-the-difference-between-a-cpu-and-a-gpu/)

Key Questions : 

- Where to run the FR application? Locally in each VM? Or only in the server? What are the pros and cons. 
- How much processing power do we need for the FR application? We need a GPU for the applying the inference file to the input? 
- Deployable and system independent is what we need in order to accommodate different professors and their systems and save on "infrastructure costs" i.e. we cannot get each professor a laptop that can run our application. 
- How exactly are we "adding known faces" to our database and how is the FR app updated in the process? Need to read into FR a bit more for this. 

**OPTION 1: Run the FR application on the Server** 

_Input to FR Application_: Frames from webcam video feed (sent at 5 min intervals to the server) 

_Output from FR Application_:  Unknown Face Trigger (sent to the dashboard)

Centralized FR Application running on the server, providing service to all the VMs. 

**Pros:** 

- It is easy to add on more Users to the system. Central server is easier to implement. Or you'll have to bake custom VM images per user basis. 

**Cons:**

- Frames need to be sent from all the VMs to the Server, at regular intervals. Can the server handle this, will there be an overhead? 
- The concept: each VM thinks it is running on a full server. In reality, one server is hosting many VMs, each of which operate independently, replacing the need for dozens of separate, dedicated, underutilized PCs. **But this system will work perfectly on the condition that not all users/ applications will require the full resources al the same time**. So will sending frames from every PC at 5 minute intervals to the FR App in the server work out? 
- Quality of the image once sent to server. 
- Probably wasting VM resources, they won't be doing anything. Might as well put FR inside. 

**OPTION 2: Run the FR application on each VM**

_Input to FR Application:_ Frames from webcam video feed (sent at 5 min intervals) 

_Output from FR Application_: Unknown Face/ Known Face (sent to the server)

Localized FR Application running on each individual VM. Only the alert (unknown face) is sent to the server. FR will be a part of the VM, give sandboxed access to the client. 

**Pros:**

- Since only the **alert** is sent to the server (which is not as frequent as frames), there is lesser resource contention, more of the VMs can run in parallel. 
- Cloning is not the problem, running them in parallel is, if there are only a limited number of users (and scalability isn't very important), then this would be better. 
- Cross platform

**Cons:**

- Deploying the FR app in each VM is cumbersome, especially if there are a lot of users. You'll have to bake custom VM images per user basis. 
- Might have compatibility issues related to the webcam access (I think this is both cases tho)
- No other cons really 

Either way, multiple VMs for each user is going to be a very expensive option. And whether or not it will make more sense to deploy the application in the VMs or in the Server really depends on how many users are there, how scalable this entire suite needs to be and to an extent can be determined only during testing. If you have like 100 users who need a 1GB VM each, then your server will be a 100GB which you will need just for the duration of paper evaluation. So this may not be cost effective? 

Software like realvnc to connect to the VMs deployed. 

**OTHER OPTIONS** 

Thought Process #1

1. Train the FR model on Google Colab, or using the system GPU, or using a Nvidia docker, if it takes 2-5 hours to train then it's cool. Anything more probably means you need more processing power than the current method you're using.

   [TensorFlow with GPU on Google Colab: Observe the difference]([TensorFlow with GPU - Colaboratory (google.com)](https://colab.research.google.com/notebooks/gpu.ipynb))

2. You now have model weights, as an inference file, which you will use in the application that you write to take an input image(in this case frames of a video). 

3. The application is Dockerized. Container image on ECR. Deployed on AWS Elastic Beanstalk, or AWS EC2 or Kubernetes. The input to the application is frames (which will be sent every 5 mins). 

4. The Exam Evaluation application runs on each VM dedicated to each Professor. This VM is accessed through the browser. And this VM also needs to have access to the camera. So the exam eval application will open and share the papers to be evaluated, turn on the camera and begin to send frames at the interval of 5 minutes as input to the public IP, and the output from the deployed app will be whether or not there is an unknown face in the image, 

Thought Process #2

Client Side Software - monitoring and take photos 

Server Side Software - verify faces and serve the papers for evaluation 

Split this up into microservices - One for auth, one for eval papers (Rest API maybe), one for FR. Build caches and MQs between them so that it can scale seamlessly with increasing number of users. 

- Papers DB and a redis cache to speedup access to the papers 

- Server for auth
- Rest API server to send papers and receive evaluated ones from users. 
- Client side will send face photos every 5 mins and it will be received at FR server, which detects the face and correlated with the auth key to tell if the registered person is the one who is in the pic. 
  - To ensure this is not overwhelmed, the FR server has a MQ backing it. The MQ will send requests to different container copies of the FR server via a load balancer. 
  - How to decide the number of copies? 1. Autoscaling, which automatically increases copies 2. Testing, and then manually set it based on users evaluating papers. You can essentially find out how many ideal copies you need only during testing. Could be 5 users per container, or 100 users per container. Whatever. 

Each can be scaled using Docker cluster or you can use kubernetes for managing what is alive and how many of it is. 

Thought Process #3 

I want isolated working environments like VMs. There are variants where you can do it in real time using sockets. 

You can also manage with GKE (Google Kubernetes Engine), which will absorb the VMs and give you a unified interface. 

