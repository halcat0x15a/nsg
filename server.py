import threading
import pickle
import SocketServer

LOGIN = 'Login'

BATTLE = 'Battle'

class Handler(SocketServer.BaseRequestHandler):

    def _login(self, data, client_ip):
        if client_ip == self.server.server_address[0] and data == BATTLE:
            self.server.mode = BATTLE
            return BATTLE
        else:
            if not self.server.players.has_key(client_ip):
                self.server.players[client_ip] = []
            return self.server.players.keys()

    def _battle(self, data, client_ip):
        self.server.players[client_ip] = data
        return self.server.players

    def handle(self):
        data = pickle.loads(self.request.recv(1024))
        client_ip = self.client_address[0]
        if self.server.mode == LOGIN:
            response = self._login(data, client_ip)
        elif self.server.mode == BATTLE:
            response = self._battle(data, client_ip)
        self.request.send(pickle.dumps(response))

class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, host, port):
        SocketServer.TCPServer.__init__(self, (host, port), Handler)
        self.mode = LOGIN
        self.players = {}
        self.socores = {}

def create_server(host, port, daemon=True):
    server = Server(host, port)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(daemon)
    server_thread.start()
    return server
