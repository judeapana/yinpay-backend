import unittest

import flask_unittest

from yinpay import create_app


class SecurityCase(flask_unittest.ClientTestCase):
    app = create_app()

    def setUp(self, client):
        pass

    def tearDown(self, client):
        pass

    def test_register(self, client): pass

    def test_login(self, client): pass

    def test_refresh(self, client): pass

    def test_logout(self, client): pass

    def test_activate_account(self, client): pass

    def change_email_address(self, client): pass


if __name__ == '__main__':
    unittest.main()
