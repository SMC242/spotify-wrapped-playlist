from yarl import URL


def spotify_url(*args, **kwargs) -> URL:
    """yarl.URL.build with the host and scheme already supplied."""
    path = kwargs.pop("path", None)
    if path.startswith("/"):
        raise ValueError("path should not start with a /")
    prefixed_path = f"/v1/{path}"
    return URL.build(host="api.spotify.com", scheme="https", path=prefixed_path, *args, **kwargs)
