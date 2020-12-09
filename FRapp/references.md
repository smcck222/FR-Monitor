**REFERENCES:** 

1. [dlib installation Linux](https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/)
   [dlib installation Windows](https://medium.com/analytics-vidhya/how-to-install-dlib-library-for-python-in-windows-10-57348ba1117f)
2. Liveness Detection : 

  - [As a binary classification problem](https://www.pyimagesearch.com/2019/03/11/liveness-detection-with-opencv/)
  - [Blink based liveness detection](https://towardsdatascience.com/real-time-face-liveness-detection-with-python-keras-and-opencv-c35dc70dafd3)
    
    A CNN was trained to classify if an eye was open or close. LeNEt-5 was trained on _Closed Eyes in the Wild (CEW)_ dataset. 
    It is composed of around 4800 eye images in size 24x24. The model gave a 94% accuracy.
    So when an eye is detected, we predict its status using the model, and keep track of the history of its status. The pattern closed-open-closed (1-0-1) indicates a blink, which in turn indicates liveness.
    
  - [Blink detection](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)

3. [Face Recognition](https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/)

