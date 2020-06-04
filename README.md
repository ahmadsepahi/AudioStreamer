# AudioStreamer
Streaming audio from multiple clients to one server or one server to multiple clients

This is a modified (and more stable) version of microphone streaming in https://gist.github.com/fopina/3cefaed1b2d2d79984ad7894aef39a68

It is tested on Ubuntu 18.04, Ubuntu 20.04, and macos with python3.

To run this program, you need to install pyaudio in both server and client systems.

###How to run
1- Run server first. The server runs on port 4444 by default. you can change the port in the code.

2- Run client: python client.py server_ip_addr server_listening_port (i.e., 4444)

###How it works
- ClientToServerStreaming streams audio from clients to a server.
- ServerToClientStreaming streams audio from a server to multiple clients.
