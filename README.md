# py-fun-misc
Misc python projects to use for resume building
Plagiarism (Plague) detection using string and document - document one is basically strings from documents. It works??

Rock, paper scissors....does game pretty well, maybe make a ui for it??

Gun-detect:
Built a python script for a gun detection program, using openCV.
Video found on youtube,GeeksForGeeks did it!

Some success, still working on the display and figuring out mistakes in using opencv. 
From GeeksForGeeks article:

Creation of Haarcascade file of Guns: 

In OpenCV, creating a Haar cascade file involves the following steps:
Prepare positive and negative images:

    We collect positive images containing the object we want to detect and negative images that do not contain the object.
    We ensure that the positive images are annotated with bounding boxes around the objects of interest.

Create a positive samples file:

    Then we will use the positive images and their annotations to create a positive samples file. This file will contain information about the positive images and their corresponding object-bounding boxes. We can use the opencv_createsamples utility to generate the positive samples file.

Create a negative samples file:

    We will create a negative samples file that lists the paths to the negative images. This file will provide information about the images that do not contain the object.

Train the cascade classifier:

    Also, we will use the positive and negative sample files to train the cascade classifier using the opencv_traincascade utility.
    Specify various parameters like the number of stages, the desired false positive rate, and the minimum and maximum object size.
    The training process will iteratively train the cascade classifier, evaluating its performance at each stage. The training may take a significant amount of time, depending on the complexity of the object and the size of the dataset.

Evaluate the trained classifier:

    After the training is complete, we can evaluate the performance of the trained cascade classifier on a separate test dataset.
    Also, we can adjust the parameters and retrain if necessary to improve the detection accuracy is needed.

Use the trained Haar cascade file:

    Once the training is successful, we will have a trained Haar cascade XML file.
    We can load this file using the cv2.CascadeClassifier class in OpenCV and use it to detect the object of interest in images or video streams.

It's important to note that training a Haar cascade classifier requires a significant amount of positive and negative samples, careful parameter tuning, and computational resources. For the simplicity of this project, we have already our cascade file. 

 Note: For The Gun haar cascade created - click here. 


the file is there buuuuuuuuuuut i want to try to make such a file first, Haar cascade XML file.

