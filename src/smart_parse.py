from typing import Iterator, Optional, List
import toolz.curried
from dataclasses import dataclass, field

# Genre names that need to be treated differently when parsing
with open("static/special_genres.txt") as f:
    special_genres = [l.strip("\n") for l in f]


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
    prefixes: List[str] = field(default_factory=list)


def make_parsed_genre(split_genre: List[str]) -> ParsedGenre:
    titlecased = list(map(str.title, split_genre))
    # No prefix
    if len(titlecased) == 1:
        return ParsedGenre(split_genre[0], split_genre[0])

    # 1 or more prefixes
    full_name = " ".join(titlecased)
    prefixes, genre = titlecased[:-1], titlecased[-1]
    return ParsedGenre(full_name, genre, prefixes)


def words(x: str) -> List[str]: return x.split(" ")


def parse_normal(genre: str) -> List[str]:
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
    for special in special_genres:
        if special.lower() in genre:
            split = parse_special(special, genre)
            break
    else:
        split = parse_normal(genre)

    return make_parsed_genre(split)


def smart_parse(genres: Iterator[str]) -> Iterator[ParsedGenre]:
    """Convert a list of genres into their components."""
    return map(parse_genre, genres)
