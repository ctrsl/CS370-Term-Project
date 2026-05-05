import mediapipe as mp
import matplotlib.pyplot as plt
import cv2 as cv
import os
import pickle #way to save data sets

#reference data from createdataset.py
DATA_DIR = './data'

#mediapipe hand drawing for detecting landmarks on hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

#model we want to use
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

#store landmarks in arrays to train
data = []
labels = []



for dir_ in os.listdir(DATA_DIR):

    #iterate through frams in directory
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):

        data_aux = []

        img = cv.imread(os.path.join(DATA_DIR, dir_, img_path))
        if img is None:
            print("Failed to load:", os.path.join(DATA_DIR, dir_, img_path))
            continue
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB) #convert image innto rgb (right now its bgr) so mediapipe can read it



        #mediapipe 
        results = hands.process(img_rgb) 
        if results.multi_hand_landmarks:
            #only detect one hand
            hand_landmarks = results.multi_hand_landmarks[0]
            #take images and make an array with information for all landmarks
            for i in range(len(hand_landmarks.landmark)):

                #each landmark store x and y and append to smaller array we will add to data after
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
    
            data.append(data_aux) #landmark data append to data at the end (this will represent an image)
            labels.append(dir_) #category

f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()
