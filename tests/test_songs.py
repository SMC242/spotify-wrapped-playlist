import unittest
from json import load
from datetime import date, datetime
from toolz import compose

import src.songs as songs


class TestSongs(unittest.TestCase):
    def setUp(self):
        with open("tests/data/playlist.json") as f:
            self.tracks = load(f)["tracks"]

    def test_added_at(self):
        expected = '2021-12-23T09:58:36Z'
        self.assertEqual(expected, songs.to_added_at(self.tracks[0]))

    def test_remove_z(self):
        input_ = '2021-12-23T09:58:36Z'
        expected = '2021-12-23T09:58:36'
        self.assertEqual(expected, songs.remove_z(input_))

    def test_parse_date(self):
        input_ = '2021-12-23T09:58:36'
        expected = datetime(year=2021, month=12, day=23,
                            hour=9, minute=58, second=36)
        self.assertEqual(expected, songs.parse_datetime(input_))

    def test_to_date(self):
        input_ = datetime(year=2021, month=12, day=23,
                          hour=9, minute=58, second=36)
        expected = date(2021, 12, 23)
        self.assertEqual(expected, songs.to_date(input_))

    def test_to_year(self):
        input_ = date(2021, 12, 23)
        expected = 2021
        self.assertEqual(expected, songs.to_year(input_))

    def test_end2end(self):
        expected = [2021, 2021, 2021]
        self.assertEqual(expected, list(songs.parse_tracks(self.tracks)))


if __name__ == '__main__':
    unittest.main()
