import cv2 as cv
import os
import sys



#create directory for training set
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 4 # how many symbols should we train
dataset_size = 200 #how many images per symbol


cap = cv.VideoCapture(0) #0 is default video capture device

if not cap.isOpened():
    print("Error: can't open webcam")
    exit()


#FOLLOWED TUTORIAL FROM https://www.youtube.com/watch?v=MJCSjXepaAM&t=178s
for j in range(number_of_classes):

    #made dirs for number of classes
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Collecting data for class {}'.format(j))

    done = False

    while True:
        ret, frame = cap.read()
        cv.putText(frame, 'Q to train', (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv.LINE_AA)
        cv.imshow('frame', frame)

        keypressed = cv.waitKey(25)  & 0xFF

        if keypressed == ord('q'):
            break
        elif keypressed == 27: #(escape) leave prematurely without training
            sys.exit() 

    #actually take images and write them to data folder
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        cv.imshow('frame', frame)
        cv.waitKey(25)
        cv.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

        counter += 1

#END OF REFERENCED CODE

cap.release()
cv.destroyAllWindows()