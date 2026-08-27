"""Atomic write helpers: write to a temp file, then rename over the target, so a
concurrent reader (e.g. the analysis server, reading the same file this
ingestion pipeline writes to) never observes a partially-written file.
`Path.replace()` (== `os.replace()`) is atomic on both POSIX and Windows -
unlike `os.rename()`, which raises on Windows if the destination already
exists."""
from pathlib import Path

import numpy as np


def atomic_write_json(path: Path, data) -> None:
    import json

    tmp_path = path.with_name(path.name + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    tmp_path.replace(path)


def atomic_write_npy(path: Path, array: np.ndarray) -> None:
    tmp_path = path.with_name(path.name + ".tmp")
    # Write through a file object, not a bare path string - np.save auto-appends
    # ".npy" to string paths that don't already end in it, which would turn
    # "foo.npy.tmp" into "foo.npy.tmp.npy".
    with open(tmp_path, "wb") as f:
        np.save(f, array)
    tmp_path.replace(path)
