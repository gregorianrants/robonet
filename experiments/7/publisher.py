from dotenv import load_dotenv
import os
from src.Hub import Hub
from src.Publisher import Publisher
import zmq
import time

load_dotenv()
print('fuck helllo')

DESKTOP_IP = os.getenv('DESKTOP_IP')

time.sleep(2)

context = zmq.Context()
publisher = Publisher(
    context=context, address=f"tcp://{DESKTOP_IP}", node="motor", topic="motor-data"
)
publisher2 = Publisher(
    context=context, address=f"tcp://{DESKTOP_IP}", node="camera", topic="frame"
)

for i in range(100):
    time.sleep(1)
    print("sending it")
    publisher.send_json({"hello": "there"})
    publisher2.send_json({"say": "cheese"})