import select

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


def callback(in_data, frame_count, time_info, status):
    try:
        s.send(in_data)
    except:
        pass
    return None, pyaudio.paContinue


stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK,
                    stream_callback=callback)

try:
    while True:
        readable, writable, errored = select.select([s], [], [])
        for ss in readable:
            data = s.recv(CHUNK)

except KeyboardInterrupt as e:
    print("keyboard", e)
    signal(SIGINT, handler)
    # pass
except:
    print("Connection disconnected")

print('Shutting down')
s.close()
stream.close()
audio.terminate()
