from dotenv import load_dotenv
import os
from Hub import Hub
from Subscriber import Subscriber
import zmq
import time

load_dotenv()

DESKTOP_IP = os.getenv('DESKTOP_IP')

time.sleep(1)

context = zmq.Context()
subscriber = Subscriber(context,node='camera',topic='frame')
subscriber.start()