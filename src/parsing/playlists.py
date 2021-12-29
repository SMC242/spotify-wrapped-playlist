from typing import Optional, List, Iterator
from re import compile
import toolz.curried as toolz


def get_playlist_id(playlist_url: str) -> Optional[str]:
    MATCH_PLAYLIST_ID = compile(r'(?<=\/playlist\/)[^?]{22}(?=\?.+|$)')

    match = MATCH_PLAYLIST_ID.search(playlist_url)
    return match.group(0) if match else None


def to_tracks(playlist_response: dict) -> list:
    """Get the track list from a playlist query"""
    return playlist_response["items"]


def to_names(tracks: Iterator[dict]) -> Iterator[str]:
    return map(toolz.get_in(["track", "name"]), tracks)


def all_tracks(pages: List[dict]) -> Iterator[dict]:
    return toolz.mapcat(to_tracks, pages)
