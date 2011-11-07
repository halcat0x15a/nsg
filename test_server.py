import unittest
import server
import client

class ServerTests(unittest.TestCase):

    def setUp(self):
        self.server = server.create_server('localhost', 0)
        self.host, self.port = self.server.server_address
        self.client = client.Client((self.host, self.port))

    def test_server(self):
        self.assertEquals(self.client.send(None)[0], self.host)
        self.assertEquals(self.client.send(server.BATTLE), server.BATTLE)
        self.assertEquals(self.client.send('Test')[self.host], 'Test')

    def tearDown(self):
        self.server.shutdown()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests((unittest.makeSuite(ServerTests)))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

