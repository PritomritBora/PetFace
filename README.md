# Petface
This is the backend functionality of the petface web application. Petface is an online platform that allows user to search about their lost pets by submitting an image
The final version of the recognition service slightly differs from the original one. Currently system does not use neural networks for feature extraction, though its use is still possible when the system becomes large enough to provide sufficient amount of training data. The release version recognition workflow is the following (Figure 3 illustrates the whole process):

-Detect face - It is done by the means of dlib python library. The method is a combination of Local Binary Pattern cascade and SVM.

-Find landmarks - Done by dlib’s shape predictor (Figure 4).

-Transform the image - The idea is to transform the image in such way that found landmarks are closely matched with the model example. This will ease the following training process.
-Obtain face’s LBP Histogram - this is the inner encoding of the face.

-Classify the face - the face is classified by the label of the most similar LBPH.

-Check similarity - correlation values of the face’s LBPH with the corresponding class’s LBPHs are compared to the inner cluster similarities. t-test decides whether the new histogram fits and either returns the cat id or one of the error codes.

Recognizer system code : 

The recognizer system is implemented in Python and extensively uses Opencv library to work with images. The code organized as a set of functions each dealing with its own part of the processing task. Below you will find the description of these functions and their API.

Besides the code some additional files are stored and used by the system. Among them are:

“lbph_face_recognizer” - trained opencv class for recognition of faces’ classes.

“predictor.dat” - trained dlib class used to detect landmarks on face images.

“visionary.net_cat_cascade_web_LBP.xml” - pretrained external cascade of simple classifiers used to detect a face on the image.

*.cim files - contain pickled lists of face images corresponding to the classes of the same name.

*.csm files - contain pickled lists of intra-class pairwise face similarities. Used to determine whether a new face really belongs to the selected class, or is it a new one.

Functions: 

TrainFaceRecognizer(folder = None) - one of the main functions designed to be called externally. It is the command to the face recognition system to retrain based on the renewed classes. It can either have a folder name as the argument - then it will assume this folder contains subfolders named after class ids with the jpeg faces of the classes - or not, then it will just use pickled images. The first case is primarily used to initialize .cim and .csm files, the latter to actually update trainers.

CheckImage(img) - the main function for the system. It takes an image as an input and returns either an id of the cat (class label) that the cat on the image belongs to, or an error code: -1 if there is a face, but of a new class, and -2 if no face was detected on the image.

FaceDetectionLBP(img) - face detection function, takes an image and outputs bounding box parameters for the face on it.

InnerSimilarity(faces) - function that takes a set of images and outputs the list of pairwise similarities between them. The similarity is calculated between Local Binary Pattern Histogram representations of the images using correlation as the similarity measure.

CalculateSimilarities(face, faces) - calculates and outputs pairwise similarities between the given face and the set of faces in the faces list.

CheckSimilarity(face, faces, classSimilarities) - this function takes a face image, a set of same class face images, and the set of their intra-class pairwise similarities and outputs a boolean value denoting whether this face really belong to the given class. This is done by performing t-test on the set of intra-class similarities and the set of the similarities between elements of the class the the new face. If the p-value is greater than the significance level (currently set to 10%), then we consider the new face as belonging to the class.

ExtractFace(img) - for the given face image tries to detect a face (using the FaceDetectionLBP(...) function) and if one is found - extracts it, finds landmarks, and transforms it so that the key landmarks lie approximately at the same spots for all the images.

RecognizeFace(face) - calls the code to find the label of class with the closest match to the new face. Outputs the label.

GetLandmarks(img, face) - returns the spots for the landmarks based on the image and face region boundaries in it.

AddClass(images, label) - creates .cim and .csm files for the new class

ModifyClass(img, label) - adds face images to the existing class, modifying the corresponding files.
