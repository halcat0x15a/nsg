import socket
import threading
import cPickle
import server

class Client(object):

    def __init__(self, address):
        self.address = address

    def send(self, data):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)
        sent = self.socket.send(cPickle.dumps(data))
        response = self.socket.recv(server.RECV_BUF)
        self.socket.close()
        return cPickle.loads(response)

    def async_send(self, data):
        thread = threading.Thread(target=lambda: self.send(data))
        thread.start()
        return thread
