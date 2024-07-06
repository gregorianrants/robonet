import asyncio
import zmq
import zmq.asyncio
from dotenv import load_dotenv
import os

load_dotenv()

DESKTOP_IP = os.getenv('DESKTOP_IP')



class Publisher():
    def __init__(self):
         self.context = zmq.asyncio.Context()
         self.req_socket = self.context.socket(zmq.REQ)
         self.req_socket.connect(f'tcp://{DESKTOP_IP}:3000')

    async def start(self):
         await self.req_socket.send_multipart([b'hello',b'there'])
         reply = await self.req_socket.recv_multipart()
         print(reply)
    


pub = Publisher()

asyncio.run(pub.start())