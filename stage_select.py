class StageSelect(object):

    def __init__(self, server, client):
        self.server = server
        self.client = client

    def draw(self):
        pass

    def action(self, controller):
        return self
