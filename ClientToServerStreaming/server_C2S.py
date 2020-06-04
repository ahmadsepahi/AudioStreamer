import pyaudio
import socket
import select
from signal import signal, SIGINT
from sys import exit

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


audio = pyaudio.PyAudio()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 4444))
serversocket.listen()


def callback(in_data, frame_count, time_info, status):
    for s in read_list[1:]:
        s.send(in_data)
    return (None, pyaudio.paContinue)


# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

read_list = [serversocket]
print("recording...")

while True:
    try:
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is serversocket:
                (clientsocket, address) = serversocket.accept()
                read_list.append(clientsocket)
                print("Connection from", address)
            else:
                data = s.recv(1024)
                stream.write(data)
                if not data:
                    read_list.remove(s)

    except KeyboardInterrupt as e:
        print("keyboard", e)
        signal(SIGINT, handler)
        print("Interrupt")
        serversocket.close()
        break

    except:
        print("client disconnected")
        # pass

print("finished recording")

serversocket.close()
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
