import zmq
import time
from collections import defaultdict
from .context import context

# class Subscriber:
#     def __init__(self, hub_ip,context, publishers):
#         self.context = context
#         self.socket = None
#         self.publishers = publishers
#         self.publisherAddresses = []
#         self.nodes = [publisher['node'] for publisher in publishers]
#         self.topics = [publisher['topic'] for publisher in publishers]
#         self.hub_socket = None
#         self.listeners = defaultdict(list)
#         self.running = True
#         self.hub_ip = hub_ip

#     def start(self):
#         self.register()
#         self.connect()

#     def getPublisherAddress(self,publisher):
#         success = False
#         while success==False:
#             self.hub_socket.send_json(
#                 {
#                         "action": "register",
#                         "register_as": "subscriber",
#                         "node": publisher['node'],
#                         "topic":publisher['topic'],
#                     }
#             )

#             message = self.hub_socket.recv_json()
#             if message["status"] == "success":
#                 success = True
#                 print("connected")
#                 return message["data"]["full_address"]
#             time.sleep(0.1)

#     def addPublisherAddress(self,address):
#         if not address in self.publisherAddresses:
#             self.publisherAddresses.append(address)

#     def register(self):
#         self.hub_socket = self.context.socket(zmq.REQ)
#         # self.hub_socket.connect("tcp://localhost:3000")
#         self.hub_socket.connect(f"tcp://{self.hub_ip}:3000")
#         for publisher in self.publishers:
#             publisherAddress = self.getPublisherAddress(publisher)
#             self.addPublisherAddress(publisherAddress)
#             print('publisherAddress:', publisherAddress)
#             print('publisherAddresses:', self.publisherAddresses)

            

#     def close(self):
#         self.running = False
#         self.socket.close()

#     def add_listener(self,topic,f):
#         self.listeners[topic].append(f)



#     def listener(self,message):
#         # time = message['time']
#         # speed = message["speed_deg/sec"]
#         # speedMonitor.udpate(speed=speed,time=time)
#         print('message')


#     def connect(self):
#         self.socket = self.context.socket(zmq.SUB)
#         for topic in self.topics:
#             self.socket.setsockopt(zmq.SUBSCRIBE, topic.encode())
#         #self.socket.setsockopt(zmq.CONFLATE, 1)
#         for publisherAddress in self.publisherAddresses:
#             print(publisherAddress)
#             self.socket.connect(publisherAddress)
            
#         while True:
#             topic,body= self.socket.recv_multipart()
#             message = zmq.utils.jsonapi.loads(body)
#             topic = topic.decode()
#             [listener(message) for listener in self.listeners[topic]]
#             #print(topic,message)
#             # self.listener(message)

class Subscriber:
    def __init__(self, hub_ip, publishers):
        self.context = context
        self.socket = None
        self.publishers = publishers
        self.publisherAddresses = []
        self.nodes = [publisher['node'] for publisher in publishers]
        self.topics = [publisher['topic'] for publisher in publishers]
        self.hub_socket = None
        self.listeners = defaultdict(list)
        self.running = True
        self.hub_ip = hub_ip

    def start(self):
        self.register()
        self.connect()

    def getPublisherAddress(self,publisher):
        success = False
        while success==False:
            self.hub_socket.send_json(
                {
                        "action": "register",
                        "register_as": "subscriber",
                        "node": publisher['node'],
                        "topic":publisher['topic'],
                    }
            )

            message = self.hub_socket.recv_json()
            if message["status"] == "success":
                success = True
                print("connected")
                return message["data"]["full_address"]
            time.sleep(0.1)

    def addPublisherAddress(self,address):
        if not address in self.publisherAddresses:
            self.publisherAddresses.append(address)

    def register(self):
        self.hub_socket = self.context.socket(zmq.REQ)
        # self.hub_socket.connect("tcp://localhost:3000")
        self.hub_socket.connect(f"tcp://{self.hub_ip}:3000")
        for publisher in self.publishers:
            publisherAddress = self.getPublisherAddress(publisher)
            self.addPublisherAddress(publisherAddress)
            print('publisherAddress:', publisherAddress)
            print('publisherAddresses:', self.publisherAddresses)

            

    def close(self):
        self.running = False
        self.socket.close()

    def add_listener(self,topic,f):
        self.listeners[topic].append(f)



    def listener(self,message):
        # time = message['time']
        # speed = message["speed_deg/sec"]
        # speedMonitor.udpate(speed=speed,time=time)
        print('message')

    #cant use json_stream and bytes stream at same time but if we really wanted to could create a 3rd stream that can handle both and it wouldnt break anything that alreday uses these.

    def json_stream(self):
         while True:
            topic,node,body= self.socket.recv_multipart()
            message = zmq.utils.jsonapi.loads(body)
            yield (topic.decode(),node.decode(),message)
            #[listener(message) for listener in self.listeners[topic]]
            #print(topic,message)
            # self.listener(message)

    def bytes_stream(self):
        while True:
            topic,node,bytes= self.socket.recv_multipart()
            yield (topic.decode(),node.decode(),bytes)
            #[listener(message) for listener in self.listeners[topic]]
            #print(topic,message)
            # self.listener(message)


    def connect(self):
        self.socket = self.context.socket(zmq.SUB)
        for topic in self.topics:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic.encode())
        #self.socket.setsockopt(zmq.CONFLATE, 1)
        for publisherAddress in self.publisherAddresses:
            print(publisherAddress)
            self.socket.connect(publisherAddress)
            
       





       
    