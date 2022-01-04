from dataclasses import dataclass
from typing import List
from abc import abstractmethod, ABCMeta


class Partial(ABCMeta):
    @abstractmethod
    def json(self) -> dict:
        raise NotImplementedError()


@dataclass
class PartialArtist(Partial):
    name: str
    artist_id: str
    url: str
    genres: List[str]

    def json(self) -> dict:
        return {
            "name": self.name,
            "id": self.artist_id,
            "url": self.url,
            "genres": self.genres
        }


@dataclass
class PartialSong(Partial):
    name: str
    artists: List[PartialArtist]
    url: str
    song_id: str

    def json(self):
        return {
            "name": self.name,
            "artists": list(map(lambda a: a.json(), self.artists)),
            "url": self.url,
            "id": self.song_id
        }
