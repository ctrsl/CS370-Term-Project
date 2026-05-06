import socket
import subprocess

HOST = "0.0.0.0"
PORT = 5000

subprocess.Popen(
        "./mjpg_streamer -i 'input_uvc.so -r 1280x720 -f 30' -o 'output_http.so -p 8080 -w ./www'",
        shell = True,
        cwd="/home/chudberrypi/mjpg-streamer/mjpg-streamer-experimental"
)

print("mjpg-streamer started on 8080")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"Listening on port {PORT}...")

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(4096).decode("utf-8").strip()
        if data:
            print(f"Received: {data}")
            subprocess.run(
                f'echo "{data}" | ./piper --model en_US-ryan-low.onnx --output_file test.wav',
                shell=True, cwd="/home/chudberrypi/piper/piper"
            )
            subprocess.run(["pw-play", "/home/chudberrypi/piper/piper/test.wav"])
    conn.close()
