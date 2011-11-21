import threading
import cPickle
import SocketServer

RECV_BUF = 8192

MENU = 'Menu'

LOGIN = 'Login'

BATTLE = 'Battle'

SCORE = 'Score'

EXIT = 'Exit'

CV = threading.Condition()

def lock():
    def decorator(f):
        def call(*args, **kw):
            with CV:
                return f(*args, **kw)
        return call
    return decorator

class Handler(SocketServer.BaseRequestHandler):

    @lock()
    def _login(self, client_ip, obj):
        self.server.players[client_ip] = None
        if client_ip == self.server.server_address[0]:
            if obj == MENU:
                self.server.mode = MENU
                CV.notify_all()
            else:
                return self.server.players.keys()
        else:
            CV.wait()
        return MENU

    @lock()
    def _menu(self, client_ip, obj):
        self.server.players[client_ip] = obj
        if all(self.server.players.values()):
            self.server.mode = BATTLE
            CV.notify_all()
        else:
            CV.wait()
        return BATTLE

    @lock()
    def _battle(self, client_ip, obj):
        self.server.players[client_ip] = obj
        living = [player for player in self.server.players.values() if player.life > 0]
        if len(living) == 1:
            self.server.players[client_ip].waiting = True
            waiting = [player.waiting for player in self.server.players.values()]
            if all(waiting):
                for key in self.server.players.keys():
                    self.server.players[key].waiting = False
                CV.notify_all()
            else:
                CV.wait()
            return SCORE
        return self.server.players

    def _score(self, client_ip, obj):
        pass

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

def create_server(host, port, performance=True, daemon=True):
    server = Server(host, port, performance)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(daemon)
    server_thread.start()
    return server
