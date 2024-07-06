from dotenv import load_dotenv
import os
from src.Hub import Hub
from src.Publisher import Publisher
import zmq
import time

load_dotenv()

DESKTOP_IP = os.getenv('DESKTOP_IP')

time.sleep(2)

context = zmq.Context()
cam_publisher = Publisher(
    context=context, address=f"tcp://{DESKTOP_IP}", node="camera", topic="frame"
)

motor_publisher = Publisher(
    context=context, address=f"tcp://{DESKTOP_IP}", node="motor", topic="speed"
)


for i in range(100):
    time.sleep(1)
    print("sending it")
    cam_publisher.send_json({"hello": "cam"})
    motor_publisher.send_json({"hello": "motor"})