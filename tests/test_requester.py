import unittest
import aiohttp
from pathlib import Path

from src.IO.requester import SpotifyRequester
from src.IO.initialise import load_secrets


class TestRequster(unittest.TestCase):
    def setUp(self):
        session = aiohttp.ClientSession()
        secrets = load_secrets(Path("secrets.json"))
        self.requester = SpotifyRequester(*secrets, session)

    def test_headers(self):
        self.requester.token = "gnomes-UwU"
        self.assertEqual({f"Authorization": "Bearer gnomes-UwU"},
                         self.requester.make_headers())


if __name__ == "__main__":
    unittest.main()
