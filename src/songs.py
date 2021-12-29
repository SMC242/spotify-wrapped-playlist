import toolz.curried as toolz
from datetime import datetime, date


def drop_last(seq): return seq[:-1]


to_added_at = toolz.get_in(["added_at"])
remove_z = drop_last
parse_datetime = datetime.fromisoformat
to_date = datetime.date
def to_year(d: datetime): return d.year


parse = toolz.compose(to_year, to_date, parse_datetime, remove_z, to_added_at)
parse_tracks = toolz.map(parse)
