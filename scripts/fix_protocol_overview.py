#!/usr/bin/env python3
"""Restore protocol/overview.md to valid UTF-8."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "content" / "docs" / "protocol" / "overview.md"

MOJIBAKE = [
    ("â€”", "—"),
    ("â€?", "—"),
    ("â†’", "→"),
    ("â”œ", "├"),
    ("â”€", "─"),
    ("â””", "└"),
    ("â”‚", "│"),
    ("â”?", "│"),
    ("â€", '"'),
    ("â€œ", '"'),
]


def main() -> None:
    raw = subprocess.check_output(
        ["git", "show", "HEAD:src/content/docs/protocol/overview.md"],
        cwd=ROOT,
    )
    text = None
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        text = raw.decode("latin-1")
    for old, new in MOJIBAKE:
        text = text.replace(old, new)
    TARGET.write_text(text, encoding="utf-8", newline="\n")
    TARGET.read_text(encoding="utf-8")
    print(f"fixed {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
