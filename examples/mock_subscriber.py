# This script is blocking
# To stop it, you might need to close the terminal window.
import zmq

ctx = zmq.Context()
socket = ctx.socket(zmq.SUB)
socket.bind("tcp://*:5002")
socket.subscribe("")

# Will receive data on port 5002 whenever available
while True:
    topic = socket.recv_string()
    print(f"\n\n{topic} => {socket.recv_json()}")
