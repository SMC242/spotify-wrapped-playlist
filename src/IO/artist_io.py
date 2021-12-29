from typing import Iterator
import toolz.curried as toolz
import asyncio

from src.IO.logger import logger
from src.IO.requester import SpotifyRequester
from src.parsing.artists import batch_ids
from src.urls.artist_urls import batched_artist_url


async def get_artists(requester: SpotifyRequester, ids: Iterator[str]) -> Iterator[dict]:
    logger.info(f"Requesting artists...")
    batched = batch_ids(ids)
    urls = map(batched_artist_url, batched)
    results = await asyncio.gather(*map(requester.get, urls))
    return toolz.mapcat(toolz.get_in(["artists"]), results)


async def songs_to_artists(requester, songs):
    ids = songs_to_artist_ids(songs)
    return await get_artists(requester, ids)
