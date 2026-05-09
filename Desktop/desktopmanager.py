import subprocess #this is for forking
import cv2 as cv
import numpy as np
import socket
from pynput import keyboard
import time
import os


currentMessage = ""
receivedMessage = ""

def sendMessage():
    global currentMessage
    print("User wants to send a message, starting subprocess")
    subprocess.run(['python3', 'testClassifiers.py'])
    with open("predicted_results.txt", "r") as f:
        content = f.read()
        print("Message to send: ", content)
    currentMessage = content
    

def receieveMessage():
    print("File Received! Reading message")
    content = ""
    with open("./Din/message.txt", "r") as file:
        content = file.read()
        print("Message read: ", content)
    img = np.zeros((200, 800, 3), dtype=np.uint8)
    cv.putText(img, content, (20,50), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv.LINE_AA)
    cv.imshow("Message", img)
    cv.waitKey(3000)#wait for a bit
    cv.destroyAllWindows()
    os.remove("./Din/message.txt")
    print("Deleted message.txt")



def main():
    global currentMessage
    print("Desktop environment started")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('172.20.10.11', 5000))
    client.settimeout(1.0)
    print("Desktop: Connected to server")

    def on_press(key):
        try:
            if key.char == 's':
                sendMessage()
        except AttributeError:
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    print("Press S to send a message")
    print("Ctrl+C to quit")

    try:
        while True:
            if currentMessage:
                client.send(currentMessage.encode('utf-8'))
                currentMessage = ""
            try:
                received = client.recv(1024).decode('utf-8').strip()
                if received:
                    print(f"Received from Pi: {received}")
                    img = np.zeros((200, 800, 3), dtype=np.uint8)
                    cv.putText(img, received, (20, 100), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv.LINE_AA)
                    cv.imshow("Received Message", img)
                    cv.waitKey(3000)
                    cv.destroyAllWindows()
            except socket.timeout:
                pass

            time.sleep(0.1)
    except KeyboardInterrupt:
        listener.stop()
        print("Shutting down")
    finally:
        client.close()


if __name__ == '__main__':
    main()
