from typing import List
from yarl import URL

from src.urls.base import spotify_url


def batched_artist_url(batch: List[str]) -> URL:
    return spotify_url(path="artists", query={"ids": ",".join(batch)})
