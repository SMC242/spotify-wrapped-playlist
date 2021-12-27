from typing import Iterator, List
import toolz.curried as toolz
from datetime import date

DictIterator = Iterator[dict]


def to_added_at(tracks: List[dict]) -> Iterator[str]:
    """Flatten a list of tracks to their added_at attribute"""
    return map(toolz.get_in(["added_at"]), tracks)


def to_date(datetime: str) -> str: return datetime.split("T")[0]
def parse_dates(xs: Iterator[str]): return map(to_date, xs)


def to_dates(xs: Iterator[str]): return map(date.fromisoformat, xs)


def to_years(xs: Iterator[date]): return map(lambda d: d.year, xs)


parse_tracks = toolz.compose(to_years, to_dates, parse_dates, to_added_at)
