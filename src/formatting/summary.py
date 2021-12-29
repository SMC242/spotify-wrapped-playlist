from typing import Iterator, Tuple
import toolz.curried


def song_lengths(
        songs: Iterator[dict]) -> Iterator[float]:
    return toolz.map(toolz.get_in(["duration_ms"], songs))


def playlist_duration(durations: Iterator[float]) -> float:
    return sum(durations)


def min_max_durations(durations: Iterator[float]) -> Tuple[float, float]:
    """Get the shortest and longest song of a playlist."""
    # Sorting it instead of calling min() and max()
    sorted_durations = sorted(durations)
    return (sorted_durations[0], sorted_durations[-1])


def summarise(playlist: dict) -> dict:
    """Get a summary of a playlist.

    Current keys:
        playlist_name: string;
        n_songs
        play_length
        shortest_song
        longest_song
    """
    name = playlist["name"]
    length = len(playlist["tracks"])
    return {}
