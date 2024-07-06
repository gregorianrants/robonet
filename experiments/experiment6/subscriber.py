from dotenv import load_dotenv
import os
from src.Hub import Hub
from src.Subscriber import Subscriber
import zmq
import time

load_dotenv()

DESKTOP_IP = os.getenv('DESKTOP_IP')

time.sleep(1)

context = zmq.Context()
subscriber = Subscriber(context,[{'node':'motor','topic':'motor-data'}])
subscriber.start()