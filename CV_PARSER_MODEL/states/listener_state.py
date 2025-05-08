from multiprocessing import Process
from utilis.ipc_socket import create_server_socket
import logging

def listener_process():
    server = create_server_socket()
    logging.info("Listener waiting for message...")
    conn, _ = server.accept()
    message = conn.recv(1024).decode()
    logging.info(f"Listener received: {message}")
    conn.close()
    server.close()

class EventListenerState:
    def run(self):
        logging.info("Starting Listener...")
        proc = Process(target=listener_process)
        proc.start()
        return proc