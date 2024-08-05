from dotenv import load_dotenv
import os
from src.Hub import Hub


load_dotenv()

DESKTOP_IP = os.getenv('DESKTOP_IP')

hub = Hub()
hub.run()

