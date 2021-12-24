import unittest
from yarl import URL

import src.playlist as playlist


class TestPlaylist(unittest.TestCase):
    def test_id(self):
        func = playlist.get_playlist_id
        self.assertEqual("58yWhVtYSYmj1bDpfNOUDq", func(
            "https://open.spotify.com/playlist/58yWhVtYSYmj1bDpfNOUDq"), "Failed normal case")
        self.assertEqual("41zvVVqoHS0N7cnTqFjvcm", func(
            "https://open.spotify.com/playlist/41zvVVqoHS0N7cnTqFjvcm?si=aap4HhEcRN-eOgCPZzmHng&utm_source=copy-link"), "Failed to ignore query")
        self.assertEqual(None, func(""), "Failed empty string case")
        self.assertEqual(None, func(
            "https://open.spotify.com/playlist/"), "Failed empty case")
        self.assertEqual(None, func(
            "https://open.spotify.com/playlist/abcdef"), "Failed too short case")
        self.assertEqual(None, func(
            "https://open.spotify.com/playlist/41zvVVqoHS0N7cnTqFjvcmjajjfjfajajffa"), "Failed too long case")

    def test_offset(self):
        func = playlist.set_offset(
            "https://api.spotify.com/v1/me/shows?offset=1&limit=1")
        self.assertEqual(URL("https://api.spotify.com/v1/me/shows?offset=2&limit=1"), func(
            2), "Failed to increment offset")
        func2 = playlist.set_offset(
            "https://api.spotify.com/v1/me/shows?limit=1")
        self.assertIn("offset=3", str(func2(
            3)), "Failed to set offset when not given")

    def test_infer(self):
        func = playlist.infer_page_urls
        page = {
            "total": 50,
            "limit": 10,
            "href": "https://api.spotify.com/v1/me/shows?offset=1&limit=10"
        }
        self.assertEqual([URL("https://api.spotify.com/v1/me/shows?offset=0&limit=10"), URL("https://api.spotify.com/v1/me/shows?offset=10&limit=10"),
                          URL("https://api.spotify.com/v1/me/shows?offset=20&limit=10"), URL("https://api.spotify.com/v1/me/shows?offset=30&limit=10"), URL("https://api.spotify.com/v1/me/shows?offset=40&limit=10")], list(func(page)), "Failed to infer pages")
        page2 = {
            "total": 40,
            "limit": 15,
            "href": "https://api.spotify.com/v1/me/shows?offset=1&limit=15"
        }
        self.assertEqual([URL("https://api.spotify.com/v1/me/shows?offset=0&limit=15"),
                          URL("https://api.spotify.com/v1/me/shows?offset=15&limit=15"), URL("https://api.spotify.com/v1/me/shows?offset=30&limit=15")], list(func(page2)), "Failed to handle uneven paging")

    def test_all_tracks_url(self):
        func = playlist.all_tracks_url
        self.assertEqual(
            URL("https://api.spotify.com/v1/playlists/1478925d/tracks?fields=items(added_at,track(artists)),next,total,limit,href,duration_ms"), func("1478925d"))


if __name__ == "__main__":
    unittest.main()
