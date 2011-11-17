import unittest
import server
import client
import nsg_object

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.server = server.create_server('localhost', 0, performance=False)
        self.host, self.port = self.server.server_address
        self.client = client.Client((self.host, self.port))
        self.gest = '192.168.1.1'

    def test_login(self):
        self.assertEquals(self.server.mode, server.LOGIN)
        self.assertEquals(len(self.client.send((self.host, None))), 1)
        self.assertTrue(self.host in self.client.send((self.host, None)))
        other_thread = self.client.async_send((self.gest, None))
        while len(self.client.send((self.host, None))) == 1:
            pass
        self.assertEquals(len(self.client.send((self.host, None))), 2)
        self.assertTrue(self.gest in self.client.send((self.host, None)))
        self.assertTrue(other_thread.is_alive())
        self.assertEquals(self.client.send((self.host, server.MENU)), server.MENU)
        other_thread.join()
        self.assertFalse(other_thread.is_alive())

    def test_menu(self):
        self.test_login()
        self.assertEquals(self.server.mode, server.MENU)
        self.host_player = nsg_object.Player()
        other_thread = self.client.async_send((self.host, self.host_player))
        self.assertTrue(other_thread.is_alive())
        self.gest_player = nsg_object.Player()
        self.assertEquals(self.client.send((self.gest, self.gest_player)), server.BATTLE)
        other_thread.join()
        self.assertFalse(other_thread.is_alive())

    def test_battle(self):
        self.test_menu()
        player = self.client.send((self.host, self.host_player))[self.host]
        self.assertEquals(player.coordinates, self.host_player.coordinates)
        self.assertEquals(player.eye, self.host_player.eye)
        self.gest_player.eye = (1, 2, 3)
        self.gest_player.coordinates = (1, 2, 3)
        player = self.client.send((self.gest, self.gest_player))[self.gest]
        self.assertEquals(player.coordinates, self.gest_player.coordinates)
        self.assertEquals(player.eye, self.gest_player.eye)

    def tearDown(self):
        self.server.shutdown()

if __name__ == '__main__':
    unittest.main()
