import toolz.curried as toolz
from typing import Iterator, List

from requester import SpotifyRequester
from artists import songs_to_artist_ids, get_artists


def to_genres(artists: Iterator[dict]) -> Iterator[str]:
    genres = toolz.mapcat(toolz.get_in(["genres"]), artists)
    return genres


async def all_genres(requester: SpotifyRequester, songs: List[dict]) -> Iterator[str]:
    artist_ids = songs_to_artist_ids(songs)
    artists = await get_artists(requester, artist_ids)
    return to_genres(artists)
