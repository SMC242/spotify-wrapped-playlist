import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Tuple, Any, Counter as CounterT
from collections import Counter
import toolz.curried as toolz

from src.songs import parse_tracks
from src.genres import all_genres


def plot_years(counter: CounterT[int]) -> None:
    breakdown = {
        "Year": list(counter.keys()),
        "Number of songs": list(counter.values()),
    }

    sns.set_theme()
    axes = sns.barplot(
        data=breakdown,
        x="Year",
        y="Number of songs",
    )
    axes.set_title("Songs per year")
    plt.show()


# Show a bar plot of the number of tracks added to the playlist per year
plot_songs_per_year = toolz.compose(
    plot_years, Counter, list, parse_tracks)


@toolz.curry
def occurs_more_than(min: int, counter: Counter) -> dict:
    return toolz.valfilter(lambda x: x > min, counter)


def sort_counter(counter: Counter) -> List[Tuple[Any, int]]:
    return sorted(counter.items(), key=lambda pair: pair[1], reverse=True)


def plot_genres(sorted_counter: List[Tuple[str, int]]) -> None:
    breakdown = {
        "Genre": list(map(toolz.get(0), sorted_counter)),
        "Occurences": list(map(toolz.get(1), sorted_counter)),
    }
    sns.set_theme()
    axes = sns.barplot(
        data=breakdown,
        x="Genre",
        y="Occurences",
    )
    axes.set_title("Most common genres")
    plt.show()


# Show a bar plot of the number of songs per genre in the playlist
plot_songs_per_genre = toolz.compose(
    plot_genres,
    sort_counter,
    occurs_more_than(10),
    Counter,
    list
)
