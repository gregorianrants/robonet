import zmq
import time
# import numpy as np
# import matplotlib.pyplot as plt


# class SpeedMonitor():
#     def __init__(self):
#         self.speeds = []
#         self.times = []

#     def udpate(self,speed,time):
#         self.speeds.append(speed)
#         self.times.append(time)

#     def show(self):
#         speeds = np.array(self.speeds)
#         times = np.array(self.times)
#         times = times -times[0]
#         plt.plot(times,speeds)
#         plt.show()


# TODO add a flag to change mode so that iterator can deal with different kinds of data
# currently recieveing bytes but we also will have subscribers that recieve json.
class Subscriber:
    def __init__(self, context, topic, node="any"):
        self.context = context
        self.socket = None
        self.publishserAddress = None
        self.subscribe_to_node = node
        self.subscribe_to_topic = topic
        self.running = True

    def start(self):
        self.register()
        self.connect()

    def register(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://localhost:3000")
        success = False

        while not success:
            socket.send_json(
                {
                    "action": "register",
                    "register_as": "subscriber",
                    "node": self.subscribe_to_node,
                    "topic": self.subscribe_to_topic,
                }
            )

            message = socket.recv_json()
            if message["status"] == "success":
                success = True
                print("connected")
                self.publishserAddress = message["data"]["full_address"]
                return message["data"]["full_address"]
            time.sleep(0.1)

    def close(self):
        self.running = False
        self.socket.close()


    def listener(self,message):
        # time = message['time']
        # speed = message["speed_deg/sec"]
        # speedMonitor.udpate(speed=speed,time=time)
        print('message')

    def connect(self):
        self.socket = self.context.socket(zmq.SUB)
        print(self.publishserAddress)
        self.socket.connect(self.publishserAddress)
        # self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        # self.socket.setsockopt(zmq.CONFLATE, 1)
        # while True:
        #     message = self.socket.recv()
        #     print(message)
        #     self.listener(message)
        # self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        # self.socket.setsockopt(zmq.CONFLATE, 1)
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.socket.setsockopt(zmq.CONFLATE, 1)
        while True:
            message = self.socket.recv()
            message = zmq.utils.jsonapi.loads(message)
            print(message)
            self.listener(message)
       
    def __next__(self):
        received_bytes = self.socket.recv_multipart()
        return received_bytes

    def __iter__(self):
        return self

