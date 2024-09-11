
import zmq
import json
import time


# class Publisher:
#     def __init__(self, hub_ip, context, address, node, topics=[]):
#         self.context = context
#         self.publicationAddress = None
#         self.socket = None
#         self.address = address
#         self.node = node
#         self.topics = topics
#         self.hub_ip = hub_ip
#         self.register()

#     def register(self):
#         socket = self.context.socket(zmq.REQ)
#         #socket.connect(f"tcp://192.168.178.23:3000")
#         socket.connect(f"tcp://{self.hub_ip}:3000")
#         socket.send_json(
#             {
#                 "action": "register",
#                 "register_as": "publisher",
#                 "topics": self.topics,
#                 "node": self.node,
#                 "address": self.address,
#             }
#         )
#         message = socket.recv_json()
#         print(message)
#         self.publicationAddress = message["data"]["full_address"]
#         self.socket = self.context.socket(zmq.PUB)
#         print(f"publisher registering to {self.publicationAddress}")
#         self.socket.bind(self.publicationAddress)

#     def send_json(self,topic,py_dict):
#         # as_json = json.dumps(py_dict)
#         # https://pyzmq.readthedocs.io/en/v17.1.0/api/zmq.utils.jsonapi.html
#         self.socket.send_multipart([topic.encode(),zmq.utils.jsonapi.dumps(py_dict)])

#     def send_bytes(self, data):
#         message = [bytes(self.node, "UTF-8"), bytes(self.topic, "UTF-8"), data]
#         # print(message)
#         self.socket.send_multipart(message)



class Publisher:
    def __init__(self, hub_ip, context, address, node, topics=[]):
        self.context = context
        self.publicationAddress = None
        self.socket = None
        self.address = address
        self.node = node
        self.topics = topics
        self.hub_ip = hub_ip
        self.register()

    def register(self):
        socket = self.context.socket(zmq.REQ)
        #socket.connect(f"tcp://192.168.178.23:3000")
        socket.connect(f"tcp://{self.hub_ip}:3000")
        socket.send_json(
            {
                "action": "register",
                "register_as": "publisher",
                "topics": self.topics,
                "node": self.node,
                "address": self.address,
            }
        )
        message = socket.recv_json()
        print(message)
        self.publicationAddress = message["data"]["full_address"]
        self.socket = self.context.socket(zmq.PUB)
        print(f"publisher registering to {self.publicationAddress}")
        self.socket.bind(self.publicationAddress)

    def send_json(self,topic,py_dict):
        # as_json = json.dumps(py_dict)
        # https://pyzmq.readthedocs.io/en/v17.1.0/api/zmq.utils.jsonapi.html
        self.socket.send_multipart([topic.encode(),self.node.encode(),zmq.utils.jsonapi.dumps(py_dict)])

    def send_bytes(self, topic,data):
        message = [topic.encode(),bytes(self.node, "UTF-8"), data]
        # print(message)
        self.socket.send_multipart(message)





