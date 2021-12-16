This script will generate some statistics about a particular Spotify playlist :)

# Plans
I intend to make this the backend for a website. It will return various graphs and tables for a given playlist.

# Currently supported stats

- Songs added per year
- Top genres

# Installation
```bash
git clone https://github.com/SMC242/spotify-wrapped-playlist.git  # Download the repo
cd spotify-wrapped-playlist
pip install -r requirements.txt
```
Then go to https://developer.spotify.com/dashboard , create an app and put your client ID and secret in `secrets.json` like this:
```json
{
	"client_id": "<clientidhere>",
	"client_secret": "<clientsecrethere>"
}
```
That will allow you to run the script locally with `python spotify-wrapped-playlist <link_to_playlist>`
