import pyaudio
import socket
import sys
from signal import signal, SIGINT
from sys import exit

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

try:
    while True:
        data = s.recv(CHUNK)
        stream.write(data)
except KeyboardInterrupt as e:
    print("keyboard", e)
    signal(SIGINT, handler)
    #pass

print('Shutting down')
s.close()
stream.close()
audio.terminate()