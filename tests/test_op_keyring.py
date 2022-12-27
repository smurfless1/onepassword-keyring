import unittest

import keyring

from onepassword_keyring import OnePasswordKeyring

expected_pass = 'passexample'
title = 'demo-service'
username = 'tarek'


class TestOnePasswordKeyringFunctional(unittest.TestCase):
    def setUp(self):
        ring = OnePasswordKeyring()
        keyring.set_keyring(ring)
        keyring.set_password(title, username, expected_pass)

    def test_reads(self):
        self.assertEqual(expected_pass, keyring.get_password(title, username))

    def test_reads_from_duplicates(self):
        self.assertTrue('U6' in keyring.get_password('Airbnb', 'business@smurfless.com'))

    def test_updates(self):
        keyring.set_password(title, username, expected_pass)

    def test_creates(self):
        keyring.set_password(title, username, expected_pass)
        self.assertEqual(expected_pass, keyring.get_password(title, username))

    def test_deletes(self):
        keyring.delete_password(title, username)


if __name__ == '__main__':
    unittest.main()
