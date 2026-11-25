#!/usr/bin/env python3
"""Write the 25 November 2026 world-news front page to /output/entry.png.

The image is bundled with this repository (entry.png) and copied byte for
byte to the output directory, so both runs of the program produce identical
bytes. Standard library only; no network access.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    with open(source, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    # A plain copy keeps the output deterministic: the same input bytes
    # always produce the same output bytes, with no timestamps involved.
    shutil.copyfile(source, target)
    os.chmod(target, 0o644)
    size = os.path.getsize(target)
    print(f"wrote {target}: {size} bytes")
    if size > 1024 * 1024:
        print("error: entry.png is over 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
