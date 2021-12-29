from typing import List, Iterator

from src.parsing.genres import to_genres
from src.parsing.artists import songs_to_artist_ids
from src.IO.artist_io import get_artists
from src.IO.requester import SpotifyRequester


async def all_genres(requester: SpotifyRequester, songs: List[dict]) -> Iterator[str]:
    artist_ids = songs_to_artist_ids(songs)
    artists = await get_artists(requester, artist_ids)
    return to_genres(artists)
