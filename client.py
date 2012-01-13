import functools
import socket
import threading
import cPickle
import server

class Client(object):

    def send(self, data, response=True):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(server.address())
        self.socket.send(cPickle.dumps(data))
        data = cPickle.loads(self.socket.recv(server.RECV_BUF)) if response else None
        self.socket.close()
        return data

