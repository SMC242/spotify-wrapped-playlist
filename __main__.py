import asyncio
import argparse

from src.initialise import get_requester
from src.playlists import get_playlist_id, request_tracks
from src.plot import plot_songs_per_year, plot_songs_per_genre
from src.genres import all_genres


def get_url() -> str:
    """Get the URL from the command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_url", type=str)
    url = parser.parse_args().playlist_url
    return url


async def main(url: str):
    requester = get_requester()
    try:
        playlist_id = get_playlist_id(url)
        if not playlist_id:
            raise ValueError("Invalid playlist URL")

        tracks = await request_tracks(requester, playlist_id)
        genres = await all_genres(requester, tracks)

        plot_songs_per_year(tracks)
        plot_songs_per_genre(genres)

    finally:
        await requester.session.close()


if __name__ == "__main__":
    url = get_url()
    if not url:
        raise RuntimeError("No playlist URL provided")
    asyncio.run(main(url))
