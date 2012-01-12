import threading
import cPickle
import SocketServer
import player

RECV_BUF = 8192

CANCEL = 'Cancel'

CHARACTER_SELECT = 'CharacterSelect'

STAGE_SELECT = 'StageSelect'

LOGIN = 'Login'

BATTLE = 'Battle'

SCORE = 'Score'

EXIT = 'Exit'

PAUSE = 'Pause'

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
        if self.server.waiting:
            self.server.players[client_ip].waiting = True
            if player.all_waiting(self.server.players):
                CV.notify_all()
                self.server.mode = CHARACTER_SELECT
                self.server.waiting = None
                for client_ip in self.server.players:
                    self.server.players[client_ip].waiting = False
            else:
                CV.wait()
            return CHARACTER_SELECT
        self.server.players[client_ip] = player.Player()
        if obj == CANCEL:
            del self.server.players[client_ip]
            return CANCEL
        elif client_ip == self.server.server_address[0]:
            if obj == CHARACTER_SELECT:
                self.server.waiting = True
                self.server.players[client_ip].waiting = True
                CV.wait()
                return CHARACTER_SELECT
            else:
                return self.server.players.keys()
        return LOGIN

    @lock()
    def _character_select(self, client_ip, obj):
        if self.server.waiting:
            self.server.players[client_ip].waiting = True
            if player.all_waiting(self.server.players):
                CV.notify_all()
                self.server.mode = STAGE_SELECT
                self.server.waiting = None
                for client_ip in self.server.players:
                    self.server.players[client_ip].waiting = False
            else:
                CV.wait()
            return STAGE_SELECT
        elif obj == CANCEL:
            self.server.players[client_ip].obj = None
            return CANCEL
        elif obj == STAGE_SELECT and client_ip == self.server.server_address[0] and all(player.objects(self.server.players)):
            self.server.waiting = True
            self.server.players[client_ip].waiting = True
            CV.wait()
            return STAGE_SELECT
        else:
            self.server.players[client_ip].obj = obj
            return CHARACTER_SELECT

    @lock()
    def _stage_select(self, client_ip, obj):
        if client_ip == self.server.server_address[0]:
            self.server.stage = obj
            self.server.mode = BATTLE
            CV.notify_all()
        else:
            CV.wait()
        return self.server.stage

    @lock()
    def _battle(self, client_ip, obj):
        if obj == PAUSE:
            self.server.waiting = client_ip
            return PAUSE
        elif self.server.waiting == client_ip:
            self.server.waiting = None
        elif self.server.waiting:
            return PAUSE
        self.server.players[client_ip].obj = obj
        if len(player.livings(self.server.players)) == 1:
            self.server.players[client_ip].waiting = True
            if player.all_waiting(self.server.players):
                for key in self.server.players.keys():
                    self.server.players[key].waiting = False
                CV.notify_all()
            else:
                CV.wait()
            return SCORE
        return player.object_dict(self.server.players)

    def _score(self, client_ip, obj):
        pass

    def _send_response(self, client_ip, obj):
        response_dict = {LOGIN: self._login, CHARACTER_SELECT: self._character_select, STAGE_SELECT: self._stage_select, BATTLE: self._battle}
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
        self.stage = None
        self.waiting = None

    def synchronize(self, client_ip, data):
        if self.waiting:
            if all(waitings(self.players)):
                CV.notify_all()
                for client_ip in self.server.players:
                    self.players[client_ip].waiting = False
            else:
                self.players[client_ip].waiting = True
                CV.wait()
            return data

def create_server(host, port, performance=True, daemon=True):
    server = Server(host, port, performance)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(daemon)
    server_thread.start()
    return server
