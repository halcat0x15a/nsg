import threading
import cPickle
import SocketServer

RECV_BUF = 8192

MENU = 'Menu'

LOGIN = 'Login'

BATTLE = 'Battle'

class Handler(SocketServer.BaseRequestHandler):

    def _login(self, client_ip, obj):
        server_ip = self.server.server_address[0]
        self.server.players[client_ip] = None
        if client_ip == server_ip:
            if obj == MENU:
                self.server.mode = MENU
                self.server.notify_all()
            else:
                return self.server.players.keys()
        else:
            self.server.wait()
        return MENU

    def _menu(self, client_ip, obj):
        self.server.players[client_ip] = obj
        if all(self.server.players.values()):
            self.server.notify_all()
            self.server.mode = BATTLE
        else:
            self.server.wait()
        return BATTLE

    def _battle(self, client_ip, obj):
        self.server.players[client_ip] = obj
        return self.server.players

    def _send_response(self, client_ip, obj):
        response_dict = {LOGIN: self._login, MENU: self._menu, BATTLE: self._battle}
        response = response_dict[self.server.mode](client_ip, obj)
        self.request.send(cPickle.dumps(response))

    def handle(self):
        data = cPickle.loads(self.request.recv(RECV_BUF))
        client_ip = self.client_address[0] if self.server.performance else data[0]
        obj = data if self.server.performance else data[1]
        self._send_response(client_ip, obj)

class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, host, port, performance):
        SocketServer.TCPServer.__init__(self, (host, port), Handler)
        self.performance = performance
        self.mode = LOGIN
        self.players = {}
        self.socores = {}
        self._cv = threading.Condition()

    def notify_all(self):
        self._cv.acquire()
        self._cv.notify_all()
        self._cv.release()

    def wait(self):
        self._cv.acquire()
        self._cv.wait()
        self._cv.release()

def create_server(host, port, performance=True, daemon=True):
    server = Server(host, port, performance)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(daemon)
    server_thread.start()
    return server
