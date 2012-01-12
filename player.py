class Player(object):

    def __init__(self):
        self.obj = None
        self.waiting = False

def object_dict(players):
    return dict([(k, v.obj) for k, v in players.items()])

def objects(players):
    return [player.obj for player in players.values()]

def all_waiting(players):
    return [player.waiting for player in players.values()]

def livings(players):
    return [player for player in players.values() if player.obj.life > 0]
