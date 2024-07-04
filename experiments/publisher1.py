from dotenv import load_dotenv
import os
from Hub import Hub
from Publisher import Publisher
import zmq
import time

load_dotenv()

DESKTOP_IP = os.getenv('DESKTOP_IP')

time.sleep(2)

context = zmq.Context()
publisher = Publisher(
    context=context, address=f"tcp://{DESKTOP_IP}", node="camera", topic="frame"
)

for i in range(100):
    time.sleep(1)
    print("sending it")
    publisher.send_json({"hello": "there"})