import toolz.curried as toolz
from typing import Iterator, List

from requester import SpotifyRequester
from artists import to_artists, get_artists


def to_genres(artists: Iterator[dict]) -> Iterator[str]:
    genres = toolz.mapcat(toolz.get_in(["genres"]), artists)
    return genres


async def all_genres(requester: SpotifyRequester, songs: List[dict]) -> Iterator[str]:
    artist_ids = map(toolz.get_in(["id"]), to_artists(songs))
    artists = await get_artists(requester, artist_ids)
    return to_genres(artists)
