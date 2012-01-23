import threading
import cPickle
import socket
import SocketServer
import player

PORT = 3939

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
    def _login(self, client_id, obj):
        if self.server.waiting:
            self.server.players[client_id].waiting = True
            if player.all_waiting(self.server.players):
                CV.notify_all()
                self.server.mode = CHARACTER_SELECT
                self.server.waiting = None
                for client_id in self.server.players:
                    self.server.players[client_id].waiting = False
            else:
                CV.wait()
            return CHARACTER_SELECT
        self.server.players[client_id] = player.Player()
        if obj == CANCEL:
            del self.server.players[client_id]
            return CANCEL
        elif client_id == self.server.identity:
            if obj == CHARACTER_SELECT:
                self.server.waiting = True
                self.server.players[client_id].waiting = True
                CV.wait()
                return CHARACTER_SELECT
            else:
                return self.server.players.keys()
        return LOGIN

    @lock()
    def _character_select(self, client_id, obj):
        if self.server.waiting:
            self.server.players[client_id].waiting = True
            if player.all_waiting(self.server.players):
                CV.notify_all()
                self.server.mode = STAGE_SELECT
                self.server.waiting = None
                for client_id in self.server.players:
                    self.server.players[client_id].waiting = False
            else:
                CV.wait()
            return STAGE_SELECT
        elif obj == CANCEL:
            self.server.players[client_id].obj = None
            return CANCEL
        elif obj == STAGE_SELECT and client_id == self.server.identity and all(player.objects(self.server.players)):
            self.server.waiting = True
            self.server.players[client_id].waiting = True
            CV.wait()
            return STAGE_SELECT
        elif obj:
            self.server.players[client_id].obj = obj
            return CHARACTER_SELECT
        else:
            return CHARACTER_SELECT

    @lock()
    def _stage_select(self, client_id, obj):
        if client_id == self.server.identity:
            self.server.stage = obj
            self.server.mode = BATTLE
            CV.notify_all()
        else:
            CV.wait()
        return self.server.stage

    @lock()
    def _battle(self, client_id, obj):
        if obj == PAUSE:
            self.server.waiting = client_id
            return PAUSE
        elif self.server.waiting == client_id:
            self.server.waiting = None
        elif self.server.waiting:
            return PAUSE
        for k, v in obj.items():
            self.server.players[k].obj = v
        if len(player.livings(self.server.players)) == 1:
            self.server.players[client_id].waiting = True
            if player.all_waiting(self.server.players):
                for key in self.server.players.keys():
                    self.server.players[key].waiting = False
                CV.notify_all()
            else:
                CV.wait()
            return SCORE
        return player.object_dict(self.server.players)

    def _score(self, client_id, obj):
        pass

    def _send_response(self, client_id, obj):
        response_dict = {LOGIN: self._login, CHARACTER_SELECT: self._character_select, STAGE_SELECT: self._stage_select, BATTLE: self._battle}
        response = response_dict[self.server.mode](client_id, obj)
        self.request.send(cPickle.dumps(response))

    def handle(self):
        data = cPickle.loads(self.request.recv(RECV_BUF))
        client_id = data[0]
        obj = data[1]
        self._send_response(client_id, obj)

class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def __init__(self, identity, host, port):
        SocketServer.TCPServer.__init__(self, (host, port), Handler)
        self.identity = identity
        self.mode = LOGIN
        self.players = {}
        self.stage = None
        self.waiting = None

def host():
    return socket.gethostbyname(socket.gethostname())

def create_server(identity, host=host(), port=PORT, daemon=True):
    server = Server(identity, host, port)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(daemon)
    server_thread.start()
    return server
