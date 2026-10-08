from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

WINDOW = 256
LOOK_AHEAD = 16
NO_NEXT_CHAR = '-'  # sentinel for null


@dataclass
class Tag:
    idx: int
    match_len: int
    addtional: str 

    def serialize(self) -> str:
        return f"({self.idx},{self.match_len},{self.addtional})"


# Greedy LZ77 encoder.
# At position i, scan the search buffer (the wind chars before i)
# and find the longest prefix of the look-ahead buffer (a[i:]) that
# also occurs there. Emit that match as a tag, advance i past it,
# and repeat.
#
# - window (wind) : how far back we're allowed to point
# - look-ahead    : how far forward we're allowed to match in one tag

def encode(seq: Iterable[str]) -> list[Tag]:

    a = "".join(seq)
    seq_len = len(a)          
    wind = WINDOW
    look = LOOK_AHEAD
    tags: list[Tag] = []

    i = 0
    while i < seq_len:
        match_len = 0               
        start = 0

        start_window = max(0, i - wind)   
        for j in range(start_window, i):
            look = LOOK_AHEAD
            k = 0
            while (j + k < seq_len          # stop on first mismatch or look = 0
                   and i + k < seq_len
                   and a[j + k] == a[i + k]
                   and look):
                k += 1
                look -= 1
            if match_len <= k:
                match_len = k
                start = j

        if not match_len:    # distinct char / first char
            t = Tag(0, 0, a[i])
        else:
            next_char = a[i + match_len] if i + match_len < seq_len else NO_NEXT_CHAR
            t = Tag(i - start, match_len, next_char)
        tags.append(t)

        i += match_len + (1 if match_len + i < seq_len else 0)

    return tags


def compressed_size(tags: list[Tag]) -> int:
    return sum(len(t.serialize()) for t in tags)