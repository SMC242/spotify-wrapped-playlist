import unittest
from json import load

import src.parsing.genres as genres


class TestGenre(unittest.TestCase):
    def setUp(self):
        with open("tests/data/artists.json") as f:
            self.artists = load(f)["artists"]

    def test_to_genres(self):
        expected = ["anime score", "japanese soundtrack"]
        self.assertEqual(expected, list(genres.to_genres(self.artists)))


if __name__ == '__main__':
    unittest.main()
