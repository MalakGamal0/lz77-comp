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
            while (j + k < seq_len          
                   and i + k < seq_len
                   and a[j + k] == a[i + k]
                   and look):
                k += 1
                look -= 1
            if match_len <= k:
                match_len = k
                start = j

        if not match_len:    
            t = Tag(0, 0, a[i])
        else:
            next_char = a[i + match_len] if i + match_len < seq_len else NO_NEXT_CHAR
            t = Tag(i - start, match_len, next_char)
        tags.append(t)

        i += match_len + (1 if match_len + i < seq_len else 0)

    return tags


def decompress(compressed_tags):
    decompressed_text = ""

    for tag in compressed_tags:
        if isinstance(tag, tuple):
            position, length, next_symbol = tag
        else:
            position, length, next_symbol = tag.idx, tag.match_len, tag.addtional

        if position == 0:
            if next_symbol and next_symbol.lower() not in ["null", "", NO_NEXT_CHAR]:
                decompressed_text += next_symbol
        else:
            for _ in range(length):
                char_to_copy = decompressed_text[-position]
                decompressed_text += char_to_copy

            if next_symbol and next_symbol.lower() not in ["null", "", NO_NEXT_CHAR]:
                decompressed_text += next_symbol

    return decompressed_text


def compressed_size(tags: list[Tag]) -> int:
    return sum(len(t.serialize()) for t in tags)
