#!/usr/bin/env python3
"""Repair pages with invalid UTF-8 bytes."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src" / "pages"

REPAIRS = [
    "go/index.astro",
    "protocol/index.astro",
    "zh-cn/protocol/index.astro",
    "ja/protocol/index.astro",
    "es/protocol/index.astro",
]

MOJIBAKE = [
    ("Ã³", "ó"),
    ("Ã¡", "á"),
    ("Ã©", "é"),
    ("Ã­", "í"),
    ("Ãº", "ú"),
    ("Ã±", "ñ"),
    ("â€?", "—"),
    ("â†?", "→"),
]


def repair(path: Path) -> None:
    raw = path.read_bytes()
    text = None
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            text = raw.decode(enc, errors="replace")
            break
    assert text is not None
    for old, new in MOJIBAKE:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8", newline="\n")
    # validate
    path.read_text(encoding="utf-8")
    print(f"repaired {path.relative_to(ROOT.parent.parent)}")


def main() -> None:
    for rel in REPAIRS:
        repair(ROOT / rel)
    # update en go hero to code-first
    go = ROOT / "go/index.astro"
    text = go.read_text(encoding="utf-8")
    text = text.replace(
        """High-performance, protocol-driven AI client. V2 standard error codes (13 codes),
              feature flags (7 features + full meta-feature), zero hardcoded provider logic,
              operator-based streaming pipeline, compile-time type safety, and sub-millisecond
              overhead.""",
        """Go protocol runtime (v1.0.0). pkg/ailib manifest HTTP chat; pkg/contact fallback policy.
              13 V2 error codes, ChatStream SSE decoder, ExecutionMetadata on responses. Go 1.21+.""",
    )
    go.write_text(text, encoding="utf-8", newline="\n")
    print("updated en go hero")


if __name__ == "__main__":
    main()
