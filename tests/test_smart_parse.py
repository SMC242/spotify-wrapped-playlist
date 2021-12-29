import unittest
from toolz import compose

import src.smart_parse as sp

parse = compose(list, sp.smart_parse)


class TestSmartParse(unittest.TestCase):
    def test_normal(self):
        input_ = ["pop", "rock", "Industrial", "REGGAE"]
        expected = [
            sp.ParsedGenre("Pop", "Pop"),
            sp.ParsedGenre("Rock", "Rock"),
            sp.ParsedGenre("Industrial", "Industrial"),
            sp.ParsedGenre("Reggae", "Reggae")
        ]
        self.assertEqual(expected, parse(input_))

    def test_prefixed(self):
        input_ = ["bedroom pop", "alternative rock"]
        expected = [
            sp.ParsedGenre("Bedroom Pop", "Pop", prefixes=["Bedroom"]),
            sp.ParsedGenre("Alternative Rock", "Rock",
                           prefixes=["Alternative"])
        ]
        self.assertEqual(expected, parse(input_))

    def test_multiple_prefixes(self):
        input_ = ["intense Swedish gnomecore", "Norwegian death metal"]
        expected = [
            sp.ParsedGenre("Intense Swedish Gnomecore",
                           "Gnomecore", ["Intense", "Swedish"]),
            sp.ParsedGenre("Norwegian Death Metal",
                           "Metal", ["Norwegian", "Death"])
        ]
        self.assertEqual(expected, parse(input_))

    def test_special(self):
        input_ = ["hip hop", "drums and bass", "POST PUNK"]
        expected = [
            sp.ParsedGenre("Hip Hop", "Hip Hop"),
            sp.ParsedGenre("Drums And Bass", "Drums And Bass"),
            sp.ParsedGenre("Post Punk", "Post Punk")
        ]
        self.assertEqual(expected, parse(input_))

    def test_prefixed_special(self):
        input_ = ["German hip hop", "alternative post punk"]
        expected = [
            sp.ParsedGenre("German Hip Hop", "Hip Hop", ["German"]),
            sp.ParsedGenre("Alternative Post Punk",
                           "Post Punk", ["Alternative"])
        ]
        self.assertEqual(expected, parse(input_))

    def test_multiple_prefixes_special(self):
        input_ = ["niche alternative goblinparty drums & bass"]
        expected = [sp.ParsedGenre("Niche Alternative Goblinparty Drums & Bass", "Drums & Bass", [
                                   "Niche", "Alternative", "Goblinparty"])]
        self.assertEqual(expected, parse(input_))


if __name__ == '__main__':
    unittest.main()
