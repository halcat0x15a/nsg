import unittest
import server
import client
import objects

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.server = server.create_server('localhost', 0, performance=False)
        self.host, self.port = self.server.server_address
        self.client = client.Client((self.host, self.port))
        self.gest_a = '192.168.1.1'
        self.gest_b = '192.168.1.2'

    def test_login(self):
        self.assertEquals(self.server.mode, server.LOGIN)
        players = self.client.send((self.host, None))
        self.assertEquals(len(players), 1)
        self.assertTrue(self.host in players)
        result = self.client.send((self.gest_a, None))
        self.assertEquals(result, server.LOGIN)
        result = self.client.send((self.gest_b, None))
        self.assertEquals(result, server.LOGIN)
        players = self.client.send((self.host, None))
        self.assertEquals(len(players), 3)
        self.assertTrue(self.gest_a in players)
        self.assertTrue(self.gest_b in players)
        result = self.client.send((self.gest_b, server.CANCEL))
        self.assertEquals(result, server.CANCEL)
        self.client.send((self.host, server.CHARACTER_SELECT), False)
        self.assertEquals(self.client.send((self.gest_a, None)), server.CHARACTER_SELECT)

    def test_character_select(self):
        self.test_login()
        self.assertEquals(self.server.mode, server.CHARACTER_SELECT)
        self.host_player = objects.Player()
        result = self.client.send((self.host, self.host_player))
        self.assertEquals(result, server.CHARACTER_SELECT)
        self.gest_a_player = objects.Player()
        result = self.client.send((self.gest_a, self.gest_a_player))
        self.assertEquals(result, server.CHARACTER_SELECT)
        result = self.client.send((self.host, server.CANCEL))
        self.assertEquals(result, server.CANCEL)
        result = self.client.send((self.host, server.STAGE_SELECT))
        self.assertEquals(result, server.CHARACTER_SELECT)
        result = self.client.send((self.host, self.host_player))
        self.assertEquals(result, server.CHARACTER_SELECT)
        self.client.send((self.host, server.STAGE_SELECT), False)
        mode = self.client.send((self.gest_a, None))
        self.assertEquals(mode, server.STAGE_SELECT)

    def test_stage_select(self):
        self.test_character_select()
        self.assertEquals(self.server.mode, server.STAGE_SELECT)
        self.client.send((self.gest_a, None), False)
        stage = self.client.send((self.host, 0))
        self.assertEquals(stage, 0)
        self.assertEquals(self.server.stage, 0)

    def test_battle(self):
        self.test_stage_select()
        self.assertEquals(self.server.mode, server.BATTLE)
        old_player = self.host_player
        self.host_player = self.client.send((self.host, self.host_player))[self.host]
        self.assertEquals(self.host_player.coordinates, old_player.coordinates)
        self.assertEquals(self.host_player.eye, old_player.eye)
        self.gest_a_player.eye = (1, 2, 3)
        self.gest_a_player.coordinates = (1, 2, 3)
        old_player = self.gest_a_player
        self.gest_a_player = self.client.send((self.gest_a, self.gest_a_player))[self.gest_a]
        self.assertEquals(self.gest_a_player.coordinates, old_player.coordinates)
        self.assertEquals(self.gest_a_player.eye, old_player.eye)
        mode = self.client.send((self.gest_a, server.PAUSE))
        self.assertEquals(mode, server.PAUSE)
        mode = self.client.send((self.host, self.host_player))
        self.assertEquals(mode, server.PAUSE)
        old_player = self.gest_a_player
        self.gest_a_player = self.client.send((self.gest_a, self.gest_a_player))[self.gest_a]
        self.assertEquals(old_player, self.gest_a_player)
        self.gest_a_player.life = 0
        self.client.send((self.gest_a, self.gest_a_player), False)
        mode = self.client.send((self.host, self.host_player))
        self.assertEquals(mode, server.SCORE)

    def tearDown(self):
        self.server.shutdown()

if __name__ == '__main__':
    unittest.main()
