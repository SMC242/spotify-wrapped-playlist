from typing import Iterator, List
#from collections.abc import Sequence
import toolz.curried as toolz
from datetime import datetime, date

DictIterator = Iterator[dict]


def to_added_at(tracks: List[dict]) -> Iterator[str]:
    """Flatten a list of tracks to their added_at attribute"""
    return map(toolz.get_in(["added_at"]), tracks)


# I couldn't get Sequence to work with mypy and strings
# so no type :,(
def drop_last(seq): return seq[:-1]


def remove_z(timestamps: Iterator[str]) -> Iterator[str]:
    return map(drop_last, timestamps)


def parse_dates(timestamps: Iterator[str]) -> Iterator[datetime]:
    return map(datetime.fromisoformat, timestamps)


def to_dates(xs: Iterator[datetime]) -> Iterator[date]:
    return map(datetime.date, xs)


def to_years(xs: Iterator[date]): return map(lambda d: d.year, xs)


parse_tracks = toolz.compose(
    to_years, to_dates, parse_dates, remove_z, to_added_at)
