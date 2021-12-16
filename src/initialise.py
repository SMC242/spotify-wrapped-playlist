from json import load
import aiohttp
from typing import Tuple

from src.requester import SpotifyRequester


def load_secrets(path: str) -> Tuple[str, str]:
    """Get the client id and secret"""
    with open(path) as f:
        json = load(f)
        return (json["client_id"], json["client_secret"])


def get_requester() -> SpotifyRequester:
    """
    Create a SpotifyRequester.
    You must remember to call requester.session.close() when you're done.
    """
    client_id, client_secret = load_secrets(
        "playlist_stats/secrets.json")
    session = aiohttp.ClientSession()
    requester = SpotifyRequester(
        client_id, client_secret, session)
    return requester
