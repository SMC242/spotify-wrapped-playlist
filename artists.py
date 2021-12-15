from typing import Set, List, Union, Iterator
from yarl import URL
import toolz.curried as toolz
import asyncio

from requester import spotify_url, SpotifyRequester

_song_to_artist = toolz.get_in(["track", "artists"])
_get_artist_id = toolz.get_in(["id"])


def to_artists(songs: List[dict]) -> Iterator[str]:
    return toolz.unique(toolz.mapcat(_song_to_artist, songs),
                        key=_get_artist_id)


def batched_artist_url(batch: List[str]) -> URL:
    return spotify_url(path="artists", query={"ids": ",".join(batch)})


async def get_artists(requester: SpotifyRequester, ids: Iterator[str]) -> Iterator[dict]:
    batched = toolz.partition_all(50, ids)
    urls = map(batched_artist_url, batched)
    results = await asyncio.gather(*map(requester.get, urls))
    return toolz.mapcat(toolz.get_in(["artists"]), results)


def songs_to_artists(requester, songs): return toolz.compose(
    toolz.curry(get_artists(requester)), to_artists)(songs)
