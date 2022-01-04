import toolz.curried as toolz
from typing import Iterator


def to_genres(artists: Iterator[dict]) -> Iterator[str]:
    genres = toolz.mapcat(toolz.get_in(["genres"]), artists)
    return genres
