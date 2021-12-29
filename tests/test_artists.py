import unittest
from json import load
from yarl impor URL

import src.artists as artists


class TestArtists(unittest.TestCase):
    def setUp(self):
        with open("tests/data/playlist.json") as f:
            self.tracks = load(f)["tracks"]

    @property
    def first_track(self) -> dict: return self.tracks[0]

    def test_song_to_artist(self):
        input_ = self.first_track
        expected = input_["track"]["artists"]
        self.assertEqual(expected, artists._song_to_artist(input_))

    def test_get_artist_id(self):
        input_ = self.first_track["track"]["artists"][0]
        expected = "0Riv2KnFcLZA3JSVryRg4y"
        self.assertEqual(expected, artists._get_artist_id(input_))

    def test_batch_ids(self):
        input_ = range(51)
        self.assertEqual(2, len(list(artists._batch_ids(input_))))

    def test_to_artists(self):
        expected = self.first_track["track"]["artists"]
        self.assertEqual(expected, list(artists.to_artists(self.tracks)))

    def test_batched_artist_url(self):
        input_ = ["coolperson42xcv", "gnomearmyg1"]
        expected = URL(
            "https://api.spotify.com/v1/artists?ids=coolperson42xcv,gnomearmyg1")
        self.assertEqual(expected, artists.batched_artist_url(input_))


if __name__ == '__main__':
    unittest.main()
