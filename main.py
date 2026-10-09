from __future__ import annotations
from pathlib import Path
import math
from lz77 import Tag, encode, compressed_size, WINDOW, LOOK_AHEAD, NO_NEXT_CHAR, decode

COMP_FILE = "comp_file"
DECOMP_FILE = "decomp_file"

def bits_needed(x: int) -> int:
    if(x == 0):
        return 1
    return x.bit_length()   


def bits_of_text(s: str) -> int:
    return len(s) * 8


def bits_of_tag(t: Tag) -> int:
    bits = 1 + bits_needed(t.idx) + bits_needed(t.match_len) + 8
    return bits

def sizeof_tags(tags: list[Tag]) -> int:
    return sum(bits_of_tag(t) for t in tags)

def read_input(source: str) -> str:
    p = Path(source)
    if p.is_file():
        return p.read_text()
    return source


def write_tags(path: str, tags: list[Tag]) -> None:
    with open(path, "w") as f:
        for t in tags:
            f.write(t.serialize() + "\n")


def parse_tags(text: str) -> list[Tag]:
    tags: list[Tag] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        inner = line.strip("()")
        idx_s, match_len_s, add = [p.strip() for p in inner.split(",", 2)]
        tags.append(Tag(int(idx_s), int(match_len_s), add))
    return tags




def read_tags(source: str) -> list[Tag]:
    p = Path(source)
    if p.is_file():
        return parse_tags(p.read_text())
    return parse_tags(source)


def do_compress() -> None:
    source = input("text or file path: ")
    text = read_input(source)

    tags = encode(text)
    write_tags(COMP_FILE, tags)

    before = bits_of_text(text)
    after  = sizeof_tags(tags)
    print(f"wrote tags to {COMP_FILE}")
    print(f"before: {before} bits")
    print(f"after:  {after} bits")
    if before:
        saved = before - after
        print(f"compressed by: {saved / before:.2%}")


def do_decompress() -> None:

    source = input ("tag file path or tag text: ") 
    tags = read_tags(source)
    result = decode(tags)
    Path(DECOMP_FILE).write_text(result)
    print(f"wrote {len(result)} chars to {DECOMP_FILE}")


def main() -> None:
    while True:
        print("\n1) compress   2) decompress   3) quit")
        choice = input("> ").strip()
        if choice == "1":
            do_compress()
        elif choice == "2":
            do_decompress()
        elif choice == "3":
            return
        else:
            print("invalid choice")


if __name__ == "__main__":
    main()
