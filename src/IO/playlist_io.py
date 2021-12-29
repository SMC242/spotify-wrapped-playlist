import asyncio
from typing import List

from src.IO.requester import SpotifyRequester
from src.IO.logger import logger
from src.parsing.playlists import all_tracks
from src.urls.playlist_urls import playlist_query, infer_page_urls


async def request_playlist(requester: SpotifyRequester, playlist_id: str) -> dict:
    """Return the information about a playlist and some information about its tracks."""
    logger.info(f"Requesting playlist {playlist_id}...")
    first_url = playlist_query(playlist_id)
    res = await requester.get(first_url)
    next_ = list(infer_page_urls(res))
    logger.debug(f"Inferred URLs {next_} from {first_url}")
    results = await asyncio.gather(*map(requester.get, next_))
    all_results = [res, *results]
    total = {**res, "tracks": list(all_tracks(all_results))}
    del total["items"]
    return total


async def request_tracks(requester: SpotifyRequester, playlist_id: str) -> List[dict]:
    playlist = await request_playlist(requester, playlist_id)
    return playlist["tracks"]
