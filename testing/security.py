import unittest

import flask_unittest
from marshmallow import pprint

from yinpay import create_app


class MyTestCase(flask_unittest.ClientTestCase):
    app = create_app()

    def setUp(self, client):
        pass

    def tearDown(self, client):
        pass

    def test_register(self, client):
        pprint(client.post('/auth/register'))


if __name__ == '__main__':
    unittest.main()
