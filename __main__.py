import toolz
import asyncio

from initialise import get_requester
from playlist import get_playlist_id, all_tracks
from plot import plot_songs_per_year, plot_songs_per_genre
from genres import all_genres

PLAYLIST_URL = 'https://open.spotify.com/playlist/41zvVVqoHS0N7cnTqFjvcm?si=e51d58bcda1c4b79'


async def main():
    try:
        requester = get_requester()
        playlist_id = get_playlist_id(PLAYLIST_URL)

        tracks = await all_tracks(requester, playlist_id)
        genres = await all_genres(requester, tracks)

        plot_songs_per_year(tracks)
        plot_songs_per_genre(genres)

    finally:
        await requester.session.close()


if __name__ == "__main__":
    asyncio.run(main())
