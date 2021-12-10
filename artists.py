from typing import Set, List, Union, Iterator
from yarl import URL
import toolz.curried as toolz
import asyncio

from requester import spotify_url, SpotifyRequester

song_to_artist = toolz.get_in(["track", "artists"])
get_artist_id = toolz.get_in(["id"])


def to_artists(songs: List[dict]) -> Iterator[str]:
    return toolz.unique(toolz.mapcat(song_to_artist, songs),
                        key=get_artist_id)


def batched_artist_url(batch: List[str]) -> URL:
    return spotify_url(path="artists", query={"ids": ",".join(batch)})


async def get_artists(requester: SpotifyRequester, ids: Iterator[str]) -> Iterator[dict]:
    batched = toolz.partition_all(50, ids)
    urls = map(batched_artist_url, batched)
    results = await asyncio.gather(*map(requester.get, urls))
    return toolz.mapcat(toolz.get_in(["artists"]), results)


def to_genres(artists: Iterator[dict]) -> Iterator[str]:
    genres = toolz.mapcat(toolz.get_in(["genres"]), artists)
    return genres

# Get the set of artist IDs
# Split into batches of 50 with toolz.partition_all https://toolz.readthedocs.io/en/latest/api.html#toolz.itertoolz.partition_all
# Use the /artists endpoint to do batched requests (up to 50)
# Request asynchronously? (using aiohttp)
# Map artist -> genres with toolz.mapcat https://toolz.readthedocs.io/en/latest/api.html#toolz.itertoolz.mapcat
# Count occurrences with toolz.frequencies https://toolz.readthedocs.io/en/latest/api.html#toolz.itertoolz.frequencies


async def all_genres(requester: SpotifyRequester, songs: List[dict]) -> Iterator[str]:
    artist_ids = map(toolz.get_in(["id"]), to_artists(songs))
    artists = await get_artists(requester, artist_ids)
    return to_genres(artists)
