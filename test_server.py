import unittest
import server
import client
import objects

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.server = server.create_server('localhost', 0, performance=False)
        self.host, self.port = self.server.server_address
        self.client = client.Client((self.host, self.port))
        self.gest = '192.168.1.1'

    def test_login(self):
        self.assertEquals(self.server.mode, server.LOGIN)
        players = self.client.send((self.host, None))
        self.assertEquals(len(players), 1)
        self.assertTrue(self.host in players)
        self.client.send((self.gest, None), False)
        players = self.client.send((self.host, None))
        self.assertEquals(len(players), 2)
        self.assertTrue(self.gest in players)
        self.assertEquals(self.client.send((self.host, server.MENU)), server.MENU)

    def test_menu(self):
        self.test_login()
        self.assertEquals(self.server.mode, server.MENU)
        self.host_player = objects.Player()
        self.client.send((self.host, self.host_player), False)
        self.gest_player = objects.Player()
        mode = self.client.send((self.gest, self.gest_player))
        self.assertEquals(mode, server.BATTLE)

    def test_battle(self):
        self.test_menu()
        host_player = self.client.send((self.host, self.host_player))[self.host]
        self.assertEquals(host_player.coordinates, self.host_player.coordinates)
        self.assertEquals(host_player.eye, self.host_player.eye)
        self.gest_player.eye = (1, 2, 3)
        self.gest_player.coordinates = (1, 2, 3)
        gest_player = self.client.send((self.gest, self.gest_player))[self.gest]
        self.assertEquals(gest_player.coordinates, self.gest_player.coordinates)
        self.assertEquals(gest_player.eye, self.gest_player.eye)
        self.gest_player.life = 0
        self.client.send((self.gest, self.gest_player), False)
        mode = self.client.send((self.host, self.host_player))
        self.assertEquals(mode, server.SCORE)

    def tearDown(self):
        self.server.shutdown()

if __name__ == '__main__':
    unittest.main()
