from json import load
import aiohttp
from typing import Tuple
from os import PathLike
from pathlib import Path

from src.IO.requester import SpotifyRequester


def load_secrets(path: PathLike) -> Tuple[str, str]:
    """Get the client id and secret"""
    with open(path) as f:
        json = load(f)
        return (json["client_id"], json["client_secret"])


def get_requester() -> SpotifyRequester:
    """
    Create a SpotifyRequester.
    You must remember to call requester.session.close() when you're done.
    """
    try:
        client_id, client_secret = load_secrets(
            Path("secrets.json"))
    except FileNotFoundError:
        raise RuntimeError("No secrets file found")
    session = aiohttp.ClientSession()
    requester = SpotifyRequester(
        client_id, client_secret, session)
    return requester
