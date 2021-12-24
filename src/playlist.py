from typing import Optional, List, Iterator
from re import compile
from math import ceil
import asyncio
import toolz.curried
from yarl import URL

from src.requester import SpotifyRequester, spotify_url

# The number of songs to request per page of a playlist
PAGE_LIMIT: int = 100


def get_playlist_id(playlist_url: str) -> Optional[str]:
    MATCH_PLAYLIST_ID = compile(r'(?<=\/playlist\/)[^?]{22}(?=\?.+|$)')

    match = MATCH_PLAYLIST_ID.search(playlist_url)
    return match.group(0) if match else None


def to_tracks(playlist_response: dict) -> list:
    """Get the track list from a playlist query"""
    return playlist_response["items"]


@toolz.curry
def set_offset(playlist_url: str, offset: int) -> URL:
    """Get a new version of a playlist URL with its song offset set to offset."""
    url = URL(playlist_url)
    path = str(url.path).replace("/v1/", "")  # spotify_url will add this again
    return spotify_url(query={**url.query, "offset": offset}, path=path)


def infer_page_urls(first_page: dict) -> Iterator[str]:
    """
    This function guesses the URLs for all of the subsequent pages
    of a playlist.

    This is necessary because the Spotify API returns results in pages.
    Each page has the URL to the next page. 
    """
    total = first_page["total"]
    # The limit produced seemed to be higher than
    items_per_page = first_page["limit"]
    n = ceil(total / items_per_page)
    # The offset is in songs, not pages
    offsets = map(lambda x: x * items_per_page, range(n))
    return map(set_offset(first_page["href"]), offsets)


def all_tracks_url(playlist_id: str) -> URL:
    fields = [
        "items(added_at,track(artists))",
        "next",
        "total",
        "limit",
        "href",
        "duration_ms",
    ]
    path = f"playlists/{playlist_id}/tracks"
    params = {"fields": ",".join(fields), }
    return spotify_url(path=path, query=params)


def all_tracks(pages: List[dict]) -> Iterator[dict]:
    return toolz.mapcat(to_tracks, pages)


async def request_playlist(requester: SpotifyRequester, playlist_id: str) -> dict:
    """Return the information about a playlist and some information about its tracks."""
    first_url = all_tracks_url(playlist_id)
    res = await requester.get(first_url)
    next_ = infer_page_urls(res)
    results = await asyncio.gather(*map(requester.get, next_))
    all_results = [res, *results]
    total = {**res, "tracks": list(all_tracks(all_results))}
    del total["items"]
    return total


async def request_tracks(requester: SpotifyRequester, playlist_id: str) -> List[dict]:
    playlist = await request_playlist(requester, playlist_id)
    return playlist["tracks"]
