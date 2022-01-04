from typing import List, Iterator
import toolz.curried as toolz

_song_to_artist = toolz.get_in(["track", "artists"])
_get_artist_id = toolz.get_in(["id"])


def to_artists(songs: List[dict]) -> Iterator[str]:
    return toolz.unique(toolz.mapcat(_song_to_artist, songs),
                        key=_get_artist_id)


songs_to_artist_ids = toolz.compose(toolz.map(_get_artist_id), to_artists)


batch_ids = toolz.partition_all(50)
