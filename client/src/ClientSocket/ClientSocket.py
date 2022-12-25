import socket
import pickle

MAX_DATA_SIZE = 1024*10


class ClientSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.client.connect((self.host, self.port))
        return self

    def __exit__(self, type, value, traceback):
        self.client.close()

    def send(self, json: dict):
        self.client.send(pickle.dumps(json))

    def recv(self):
        return pickle.loads(self.client.recv(MAX_DATA_SIZE), encoding='utf-8')
