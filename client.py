import socket
import pickle

class Client(object):

    def __init__(self, address):
        self.address = address

    def send(self, data):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)
        sent = self.socket.send(pickle.dumps(data))
        response = self.socket.recv(1024)
        self.socket.close()
        return pickle.loads(response)
