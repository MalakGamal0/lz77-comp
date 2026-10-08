from __future__ import annotations
from pathlib import Path
import math
from lz77 import Tag, encode, compressed_size, WINDOW, LOOK_AHEAD, NO_NEXT_CHAR

COMP_FILE = "comp_file"
BITS_PER_CHAR = 8


OFFSET_BITS = math.ceil(math.log2(WINDOW + 1))          # offset 1..WINDOW
LENGTH_BITS = math.ceil(math.log2(LOOK_AHEAD + 1))      # len 1..LOOK_AHEAD
FLAG_BITS   = 1                                         # literal vs match
HAS_NEXT_BITS = 1                                       # next char present?
LITERAL_BITS = FLAG_BITS + BITS_PER_CHAR                # 9
MATCH_BITS  = FLAG_BITS + OFFSET_BITS + LENGTH_BITS + HAS_NEXT_BITS


def bits_of_text(s: str) -> int:
    return len(s) * BITS_PER_CHAR


def bits_of_tags(tags: list[Tag]) -> int:
    total = 0
    for t in tags:
        if t.idx == 0 and t.match_len == 0:
            total += LITERAL_BITS
        else:
            total += MATCH_BITS
            if t.addtional != NO_NEXT_CHAR:
                total += BITS_PER_CHAR
    return total


def read_input(source: str) -> str:
    p = Path(source)
    if p.is_file():
        return p.read_text()
    return source


def write_tags(path: str, tags: list[Tag]) -> None:
    with open(path, "w") as f:
        for t in tags:
            f.write(t.serialize() + "\n")


def do_compress() -> None:
    source = input("text or file path: ")
    text = read_input(source)

    tags = encode(text)
    write_tags(COMP_FILE, tags)

    before = bits_of_text(text)
    after  = bits_of_tags(tags)
    print(f"wrote tags to {COMP_FILE}")
    print(f"before: {before} bits")
    print(f"after:  {after} bits")
    if before:
        saved = before - after
        print(f"compressed by: {saved / before:.2%}")


def main() -> None:
    while True:
        print("\n1) compress   2) quit")
        choice = input("> ").strip()
        if choice == "1":
            do_compress()
        elif choice == "2":
            return
        else:
            print("invalid choice")


if __name__ == "__main__":
    main()