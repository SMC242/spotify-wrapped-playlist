import asyncio
import argparse

from src.initialise import get_requester
from src.playlist import get_playlist_id, all_tracks
from src.plot import plot_songs_per_year, plot_songs_per_genre
from src.genres import all_genres


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_url", type=str)
    url = parser.parse_args().playlist_url

    try:
        requester = get_requester()
        playlist_id = get_playlist_id(url)

        tracks = await all_tracks(requester, playlist_id)
        genres = await all_genres(requester, tracks)

        plot_songs_per_year(tracks)
        plot_songs_per_genre(genres)

    finally:
        await requester.session.close()


if __name__ == "__main__":
    asyncio.run(main())
