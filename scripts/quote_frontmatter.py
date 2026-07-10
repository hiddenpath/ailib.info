#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src" / "content" / "docs"


def main() -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("---", 3)
        if end < 0:
            continue
        fm = text[3:end]
        changed = False

        def quote(m: re.Match[str]) -> str:
            nonlocal changed
            key, val = m.group(1), m.group(2).strip()
            if val.startswith(('"', "'")):
                return m.group(0)
            if ":" in val:
                changed = True
                escaped = val.replace('"', '\\"')
                return f'{key}: "{escaped}"'
            return m.group(0)

        new_fm = re.sub(r"^(title|description):\s*(.+)$", quote, fm, flags=re.M)
        if changed:
            path.write_text("---" + new_fm + text[end:], encoding="utf-8", newline="\n")
            print(f"quoted {path.relative_to(ROOT)}")
    print("done")


if __name__ == "__main__":
    main()
