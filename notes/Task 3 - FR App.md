**References:** 

1. [Tensorflow with GPU](https://colab.research.google.com/notebooks/gpu.ipynb)

2. [FR System Reference](https://machinelearningmastery.com/how-to-develop-a-face-recognition-system-using-facenet-in-keras-and-an-svm-classifier/)

3. [A Gentle Introduction to Deep Learning for Face Recognition (machinelearningmastery.com)](https://machinelearningmastery.com/introduction-to-deep-learning-for-face-recognition/))

4. Read about different FR products (Ari will share) and see what they do. Check out the issues with those because we want to build a mature product, which is robust.

5. [Vichu's Link](https://youtu.be/bgfxXe1u1eM)

6. Madhav's Stuff: Liveness Detection + FR unknown face. 

7. Figure out a way to send JSON output to dashboard. 

   - Send label alone 
   - Send frame + label. How to send the frame, take care of it later. 

**Points to Remember: ** 

1. The paper viewing and eval is not part of our app. 
2. User should not know that our app is running (no UI on user end). 
3. Get admin access to computer to make sure user does not switch off. 
4. Convert face data and label to json for transmission to dashboard. 
5. Check if DB is required for JSON storage if many VMs are running. 
   

