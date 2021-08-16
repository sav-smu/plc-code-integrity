import time
import zmq

ctx = zmq.Context()
socket = ctx.socket(zmq.PUB)
socket.bind("tcp://*:6002")

data = {
    "Timestamp": int(time.time()),
    "LIT101": 1000,
    "LIT301": 500,
    "FIT101": 2.5,
    "FIT301": 0.0,
    "data_source": "MOCK"
}

# Will publish data every second for tags to use
while True:
    socket.send_string("#PlantIO#", flags=zmq.SNDMORE)
    socket.send_json(data)
    data["Timestamp"] = int(time.time())
    time.sleep(1)
