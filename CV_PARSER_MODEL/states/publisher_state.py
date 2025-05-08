import time
from utilis.ipc_socket import create_client_socket
import logging

class EventPublisherState:
    def run(self):
        time.sleep(1)  # Wait for listener to be ready
        try:
            client = create_client_socket()
            msg = "Hello from Publisher!"
            client.send(msg.encode())
            logging.info(f"Publisher sent: {msg}")
            client.close()
            return True
        except Exception as e:
            logging.error(f"Publisher failed: {e}")
            return False