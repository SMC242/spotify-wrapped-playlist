from typing import Tuple, List
from json import load
import toolz
import aiohttp
import asyncio

from requester import SpotifyRequester
from playlist import get_playlist_id, all_tracks
from plot import plot_songs_per_year, plot_songs_per_genre
from artists import all_genres

PLAYLIST_URL = 'https://open.spotify.com/playlist/41zvVVqoHS0N7cnTqFjvcm?si=e51d58bcda1c4b79'


def load_secrets(path: str) -> Tuple[str, str]:
    """Get the client id and secret"""
    with open(path) as f:
        json = load(f)
        return (json["client_id"], json["client_secret"])


async def main():
    client_id, client_secret = load_secrets("secrets.json")
    async with aiohttp.ClientSession() as session:
        requester = SpotifyRequester(
            client_id, client_secret, session)
        playlist_id = get_playlist_id(PLAYLIST_URL)
        tracks = await all_tracks(requester, playlist_id)

        plot_songs_per_year(tracks)

        genres = await all_genres(requester, tracks)
        plot_songs_per_genre(genres)


if __name__ == "__main__":
    asyncio.run(main())
