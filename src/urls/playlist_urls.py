import toolz.curried as toolz
from math import ceil
from typing import Iterator
from yarl import URL

from src.formatting.fields import Fields
from src.urls.base import spotify_url

# The number of songs to request per page of a playlist
PAGE_LIMIT: int = 100
DEFAULT_FIELDS = Fields(
    "next",
    "total",
    "limit",
    "href",
    "duration_ms",
    Fields("added_at", Fields("artists", "name",
                              title="track"), title="items")
)


def playlist_query(playlist_id: str, fields: Fields = None) -> URL:
    path = f"playlists/{playlist_id}/tracks"
    params = {
        "fields": (fields or DEFAULT_FIELDS).construct(),
        "offset": 0,
        "limit": PAGE_LIMIT,
    }
    return spotify_url(path=path, query=params)


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
    # The offset is in songs, not pages so I have to multiply
    items_per_page = first_page["limit"]
    n = ceil(total / items_per_page)
    # Starting from 1 because the first page was already requested
    offsets = map(lambda x: x * items_per_page, range(1, n))
    return map(set_offset(first_page["href"]), offsets)
