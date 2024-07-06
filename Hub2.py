import asyncio
import zmq
import zmq.asyncio
from dotenv import load_dotenv
import os


load_dotenv()

DESKTOP_IP = os.getenv('DESKTOP_IP')


class Hub():
    def __init__(self):
        self.context = zmq.asyncio.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind('tcp://*:3001')

        self.rep_socket = self.context.socket(zmq.REP)
        
        self.publishers = []

    def add_topic_publisher(self,publisher):
        self.publishers.append()

    async def publisher_registration_loop(self):
        self.rep_socket.bind('tcp://*:3000')
        while True:
            msg = await self.rep_socket.recv_multipart()
            print(msg)
            await asyncio.sleep(1)
            await self.rep_socket.send_multipart([b'topic',b'my reply'])

hub = Hub()

asyncio.run(hub.publisher_registration_loop())