from typing import Any, Iterator, Optional, List
from collections.abc import Sequence
from bisect import bisect_left
import toolz.curried
from dataclasses import dataclass, field


def binary_search(arr: Sequence, x: Any) -> int:
    i = bisect_left(arr, x)
    if i != len(arr) and arr[i] == x:
        return i
    else:
        return -1


def get_searcher(arr: Sequence):
    """Sort a sequence and get a function that will search through it."""
    @toolz.curry
    def searcher(xs: Sequence, x: Any) -> int:
        return binary_search(xs, x)
    return searcher(sorted(arr))


@dataclass
class ParsedGenre:
    """ 
    A genre name that has been split into its components.

    full_name:
        The original name of the genre
    genre:
        The broad genre
    prefixes:
        The prefixes added to a genre to make a subgenre
    """
    full_name: str
    genre: str
    prefixes: Optional[List[str]] = None


def make_parsed_genre(split_genre: List[str]) -> ParsedGenre:
    # No prefix
    if len(split_genre) == 1:
        return ParsedGenre(split_genre[0], split_genre[0])

    # 1 or more prefixes
    full_name = " ".join(split_genre)
    prefixes, genre = split_genre[:-1], split_genre[-1]
    return ParsedGenre(full_name, genre, prefixes)


# Genre names that need to be treated differently when parsing
SPECIAL_GENRES = [
    "hip hop"
]


def words(x: str) -> List[str]: return x.split(" ")


def parse(genre: str) -> List[str]:
    split = words(genre)
    if len(split) > 1:
        # Assume the last word is the genre name
        return [*split[:-1], split[-1]]
    return split


def parse_special(expected: str, actual: str) -> List[str]:
    """Reconstruct a special genre name."""
    split_expected, split_actual = words(expected), words(actual)
    start = split_actual.index(split_expected[0])
    # Assume all words after the start are part of the genre name
    reconstructed = " ".join(split_actual[start:])
    return [*split_actual[:start], reconstructed]


def parse_genre(genre: str) -> ParsedGenre:
    """Convert a genre into its components."""
    for special in SPECIAL_GENRES:
        if special in genre:
            split = parse_special(special, genre)
            break
    else:
        split = parse(genre)

    return make_parsed_genre(split)


def smart_parse(genres: Iterator[str]) -> Iterator[ParsedGenre]:
    """Convert a list of genres into their components."""
    searcher = get_searcher(list(toolz.unique(genres)))
    return map(parse_genre, genres)
