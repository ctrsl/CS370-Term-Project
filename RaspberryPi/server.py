import socket
import subprocess
import speech_recognition as sr
import threading

HOST = "0.0.0.0"
PORT = 5000

subprocess.Popen(
    "./mjpg_streamer -i 'input_uvc.so -r 1280x720 -f 30' -o 'output_http.so -p 8080 -w ./www'",
    shell=True,
    cwd="/home/chudberrypi/mjpg-streamer/mjpg-streamer-experimental"
)
print("mjpg-streamer started on 8080")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"Listening on port {PORT}...")

conn = None

def listen_and_send():
    global conn
    if conn is None:
        print("No client connected, can't send")
        return
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("Recording...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 2.0
        audio = recognizer.listen(source, phrase_time_limit=15)
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        conn.send(text.encode('utf-8'))
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")

def key_listener():
    print("Press R then Enter to record speech and send to desktop")
    while True:
        ch = input()
        if ch.lower() == 'r':
            threading.Thread(target=listen_and_send).start()

threading.Thread(target=key_listener, daemon=True).start()

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")
    conn.settimeout(1.0)
    while True:
        try:
            data = conn.recv(4096).decode("utf-8").strip()
            if not data:
                print("Client disconnected")
                break
            if data:
                print(f"Received: {data}")
                subprocess.run(
                    f'echo "{data}" | ./piper --model en_US-ryan-low.onnx --output_file test.wav',
                    shell=True, cwd="/home/chudberrypi/piper/piper"
                )
                subprocess.run(["pw-play", "/home/chudberrypi/piper/piper/test.wav"])
        except socket.timeout:
            pass
    conn.close()
