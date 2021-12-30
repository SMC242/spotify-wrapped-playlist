import aiohttp
import requests
import asyncio
from typing import Callable, Union
from yarl import URL

from src.IO.logger import logger


class SpotifyRequester:
    def __init__(self, client_id: str, client_secret: str, session: aiohttp.ClientSession):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = session
        self.token = self.get_token()
        self.auth_headers = self.make_headers()

    def get_token(self) -> str:
        """
        Synchronously get the authorisation token.

        This must be synchronous, otherwise calls to `get` will fail.
        """
        logger.info("Authenticating...")
        AUTH_URL = 'https://accounts.spotify.com/api/token'
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        res = requests.post(AUTH_URL, payload)
        if not res.ok:
            logger.fatal("Failed to get authorisation token")
        return res.json()["access_token"]

    def make_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    async def get(self, url: Union[str, URL], params: dict = None) -> dict:
        logger.debug(f"Requesting {url} with {params=}")
        async with self.session.get(url, headers=self.auth_headers, params=params) as res:
            if not res.ok:
                logger.error(
                    f"Request to {url} failed with code {res.status} for reason {res.reason}")

            return await res.json()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        await self.session.close()
