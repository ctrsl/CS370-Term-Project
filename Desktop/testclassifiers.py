#test the classifiers we train in trainclassifiers.py (camera class)

import cv2 as cv
from mjpeg_streamer import MjpegServer, Stream
import mediapipe as mp
import numpy as np
import pickle


model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

labels_dict = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z',
    26: '0',
    27: '1',
    28: '2',
    29: '3',
    30: '4',
    31: '5',
    32: '6',
    33: '7',
    34: '8',
    35: '9',
}

#mediapipe hand drawing for detecting landmarks on hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

#model we want to use
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

cap = cv.VideoCapture(0)

#Predict results and write them to an array.
predicted_results = []

while True:

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB) #convert image innto rgb (right now its bgr) so mediapipe can read it

    #mediapipe drawing
    results = hands.process(frame_rgb) 
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            #model data
            data_aux = []

            #for drawing hand
            x_ = []
            y_ = []

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            
            #take images and make an array with information for all landmarks
            for i in range(len(hand_landmarks.landmark)):
                #each landmark store x and y and append to smaller array we will add to data after
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
                #for drawing  rectangle prediction
                x_.append(x)
                y_.append(y)

            #for drawing  rectangle prediction
            x1 = int(min(x_) * W)
            y1 = int(min(y_) * H)

            x2 = int(max(x_) * W)
            y2 = int(max(y_) * H)

            prediction = model.predict([np.asarray(data_aux)])

            #draw prediction on top of frame with dict
            predicted_character = labels_dict[int(prediction[0])]
            cv.rectangle(frame, (x1, y1), (x2, y2), (0,0,0), 4)
            cv.putText(frame, predicted_character, (x1,y1), cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv.LINE_AA)
            
            legend = [
                "[TAB] record a symbol",
                "[B] Backspace",
                "[SPACE] Space",
                "[ENTER] Save File",
                "[Q] Exit",
            ]
            y0, dy = 50, 40
            for i, legend in enumerate(legend):
                y = y0 + i * dy
                cv.putText(frame, legend, (50, y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1, cv.LINE_AA)
            key = cv.waitKey(1) & 0xFF
            if key == ord("b"):
                if not predicted_results:    
                    print("Nothing to remove! Precition result list is empty.")
                else:
                    predicted_results.pop()
                    print("Removed last element. Current string:", predicted_results)
            elif key == 9:  # Tab
                predicted_results.append(predicted_character)
                print("Recording predicted character: ", predicted_character, "Result: ", predicted_results)
            elif key == 32: # Space
                predicted_results.append(" ")
                print("Recorded a space, ", predicted_results)
                


    cv.imshow("MJPEG Stream", frame)

    # Call it once per loop
    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    elif key == 13: # Enter
        if not predicted_results:    
            print("Nothing to write! Precition result list is empty.")
        else:
            print("Saving predicted_results to file and clearing list for next message")
            with open("predicted_results.txt", "w") as f:
                for item in predicted_results:
                    f.write(item)
    predicted_results.clear()
    



cap.release()
cv.destroyAllWindows()