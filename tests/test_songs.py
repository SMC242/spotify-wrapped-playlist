import unittest
from json import load
from datetime import date
from toolz import compose

import src.songs as songs


class TestSongs(unittest.TestCase):
    def setUp(self):
        with open("tests/data/playlist.json") as f:
            self.tracks = load(f)["tracks"]

    def test_added_at(self):
        expected = ['2021-12-23T09:58:36Z',
                    '2021-12-23T09:58:46Z', '2021-12-23T09:58:51Z']
        self.assertEqual(expected, list(songs.to_added_at(self.tracks)))

    def test_parse_dates(self):
        input_ = ['2021-12-23T09:58:36Z',
                  '2021-12-23T09:58:46Z', '2021-12-23T09:58:51Z']
        expected = ['2021-12-23', '2021-12-23', '2021-12-23']
        self.assertEqual(expected, list(songs.parse_dates(input_)))

    def test_to_dates(self):
        input_ = ['2021-12-23', '2021-12-23', '2021-12-23']
        expected = [date(2021, 12, 23), date(2021, 12, 23), date(2021, 12, 23)]
        self.assertEqual(expected, list(songs.to_dates(input_)))

    def test_to_years(self):
        input_ = [date(2021, 12, 23), date(2021, 12, 23), date(2021, 12, 23)]
        expected = [2021, 2021, 2021]
        self.assertEqual(expected, list(songs.to_years(input_)))


if __name__ == '__main__':
    unittest.main()
