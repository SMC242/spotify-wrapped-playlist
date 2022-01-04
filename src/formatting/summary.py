from typing import Iterator, Tuple
import toolz.curried

song_duration = toolz.get_in(["duration_ms"])
song_lengths = toolz.map(song_duration)
total_duration = toolz.compose(sum, song_lengths)


def min_max_durations(tracks: Iterator[dict]) -> Tuple[dict, dict]:
    """Get the shortest and longest song of a playlist."""
    sorted_durations = sorted(tracks, key=song_duration)
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
    tracks = playlist["tracks"]
    name = playlist["name"]
    length = len(tracks)
    duration = total_duration(tracks)
    shortest, longest = min_max_durations(tracks)
    return {
        "playlist_name": name,
        "n_songs": length,
        "play_length": duration,
        "shortest_song": shortest,
        "longest_song": longest
    }
