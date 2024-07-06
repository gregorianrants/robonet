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

class Subscriber:
    def __init__(self, context, publishers):
        self.context = context
        self.socket = None
        self.publishers = publishers
        self.publisherAddresses = []
        self.nodes = [publisher['node'] for publisher in publishers]
        self.topics = [publisher['topic'] for publisher in publishers]
       
        self.running = True

    def start(self):
        self.register()
        self.connect()

    def register(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://localhost:3000")
        for publisher in self.publishers:
            success = False
            while success==False:
                socket.send_json(
                    {
                            "action": "register",
                            "register_as": "subscriber",
                            "node": publisher['node'],
                            "topic":publisher['topic'],
                        }
                )

                message = socket.recv_json()
                if message["status"] == "success":
                    success = True
                    print("connected")
                    self.publisherAddresses.append(message["data"]["full_address"])
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
        for topic in self.topics:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic.encode())
        #self.socket.setsockopt(zmq.CONFLATE, 1)
        for publisherAddress in self.publisherAddresses:
            print(publisherAddress)
            self.socket.connect(publisherAddress)
            
        while True:
            topic,body= self.socket.recv_multipart()
            message = zmq.utils.jsonapi.loads(body)
            topic = topic.decode()
            print(topic,message)
            # self.listener(message)
       
    