#!/usr/bin/env python3
"""Ship the 25 November 2026 front page as this entry's output.

The repository carries the finished picture (entry.png). This program
checks that it really is a PNG, then writes those exact bytes into the
directory the grader reads. A byte-for-byte copy is deterministic by
construction: the same input always yields the same output. It uses
only the standard library and fetches nothing from the network.
"""

import os
from pathlib import Path

PICTURE = "entry.png"
SIZE_LIMIT = 1024 * 1024
PNG_SIGNATURE = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))


def picture_path() -> Path:
    return Path(__file__).resolve().with_name(PICTURE)


def read_picture() -> bytes:
    blob = picture_path().read_bytes()
    if blob[:8] != PNG_SIGNATURE:
        raise SystemExit(f"error: {PICTURE} does not start with a PNG signature")
    if len(blob) > SIZE_LIMIT:
        raise SystemExit(
            f"error: {PICTURE} is {len(blob)} bytes, over the 1 MiB limit")
    return blob


def output_dir() -> Path:
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target.mkdir(parents=True, exist_ok=True)
    return target


def publish(blob: bytes) -> Path:
    destination = output_dir() / PICTURE
    destination.write_bytes(blob)
    destination.chmod(0o644)
    # Read it back: the graded run must see exactly the bytes we shipped.
    if destination.read_bytes() != blob:
        raise SystemExit(f"error: {destination} did not round-trip cleanly")
    return destination


def main() -> int:
    blob = read_picture()
    destination = publish(blob)
    print(f"published {destination} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
