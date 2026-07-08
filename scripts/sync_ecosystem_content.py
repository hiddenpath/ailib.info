#!/usr/bin/env python3
"""One-shot content sync for AILIB-004 — UTF-8 safe bulk replacements."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src"

REPLACEMENTS: list[tuple[str, str]] = [
    # npm scope migration
    ("@hiddenpath/ai-lib-ts", "@ailib-official/ai-lib-ts"),
    ("@hiddenpath/ai-protocol", "@ailib-official/ai-protocol"),
    # ecosystem matrix
    ("ai-lib-rust v0.9.6", "ai-lib-rust v1.0.1"),
    ("ai-lib-python v0.7.4", "ai-lib-python v1.0.0"),
    ("ai-lib-ts v0.5.3", "ai-lib-ts v1.0.0"),
    ("ai-lib-rust v1.0.0", "ai-lib-rust v1.0.1"),
    ("**ai-lib-rust** (v1.0.0)", "**ai-lib-rust** (v1.0.1)"),
    ("- **ai-lib-rust** (v1.0.0)", "- **ai-lib-rust** (v1.0.1)"),
    ("| v1.0.0  | [Crates.io]", "| v1.0.1  | [Crates.io]"),
    # runtime doc version headers
    ("ai-lib-rust v0.8.0", "ai-lib-rust v1.0.1"),
    ("ai-lib-rust (v0.8.0)", "ai-lib-rust (v1.0.1)"),
    ("ai-lib-rust（v0.8.0）", "ai-lib-rust（v1.0.1）"),
    ("**ai-lib-rust** (v0.8.0)", "**ai-lib-rust** (v1.0.1)"),
    ("**ai-lib-rust**（v0.8.0）", "**ai-lib-rust**（v1.0.1）"),
    ("ai-lib-python v0.7.0", "ai-lib-python v1.0.0"),
    ("ai-lib-python (v0.7.0)", "ai-lib-python (v1.0.0)"),
    ("ai-lib-python（v0.7.0）", "ai-lib-python（v1.0.0）"),
    ("**ai-lib-python** (v0.7.0)", "**ai-lib-python** (v1.0.0)"),
    ("**ai-lib-python**（v0.7.0）", "**ai-lib-python**（v1.0.0）"),
    ("ai-lib-python (v0.7.0+)", "ai-lib-python (v1.0.0+)"),
    ("ai-lib-python（v0.7.0+）", "ai-lib-python（v1.0.0+）"),
    ("ai-lib-python v0.7.0+", "ai-lib-python v1.0.0+"),
    ("ai-lib-go v0.5.0", "ai-lib-go v1.0.0"),
    ("ai-lib-go (v0.5.0)", "ai-lib-go (v1.0.0)"),
    ("ai-lib-go（v0.5.0）", "ai-lib-go（v1.0.0）"),
    # install pins
    ("ai-lib-python>=0.8.0", "ai-lib-python>=1.0.0"),
    ("ai-lib-python[full]>=0.8.0", "ai-lib-python[full]>=1.0.0"),
    ("ai-lib-python>=0.7.0", "ai-lib-python>=1.0.0"),
    ("v0.7.0 fully implements", "v1.0.0 fully implements"),
    ("v0.7.0 与 AI-Protocol", "v1.0.0 与 AI-Protocol"),
    ("v0.7.0 は AI-Protocol", "v1.0.0 は AI-Protocol"),
    ("v0.7.0 está alineado", "v1.0.0 está alineado"),
    ("# Basic installation (v0.8.0+)", "# Basic installation (v1.0.0+)"),
    ("# 基本インストール（v0.7.0+）", "# 基本インストール（v1.0.0+）"),
    ("# Basic installation (v0.7.0+)", "# Basic installation (v1.0.0+)"),
    # showcase
    ('version="1.0.0"\r\n              title="ai-lib-rust"', 'version="1.0.1"\r\n              title="ai-lib-rust"'),
    ('version="0.3.0"\r\n                title="SpiderSwitch"', 'version="0.4.2"\r\n                title="SpiderSwitch"'),
]

# Fix go overview "early development" copy
GO_OVERVIEW_EN = (
    "The Go SDK is currently in early development (v0.5.0) but implements the core Ring 1/Ring 2 features of the V2 specification:",
    "The Go SDK (v1.0.0) is the Wave-5 stable runtime and implements the core Ring 1/Ring 2 features of the V2 specification:",
)
GO_OVERVIEW_ZH = (
    "Go SDK 目前处于早期开发阶段 (v0.5.0)，但实现了 V2 规范的核心 Ring 1/Ring 2 功能：",
    "Go SDK（v1.0.0）为 Wave-5 稳定版，实现了 V2 规范的核心 Ring 1/Ring 2 功能：",
)
GO_OVERVIEW_JA = (
    "Go SDK は現在初期開発段階 (v0.5.0) ですが、V2 仕様のコアである Ring 1/Ring 2 機能を実装しています：",
    "Go SDK（v1.0.0）は Wave-5 安定版で、V2 仕様のコアである Ring 1/Ring 2 機能を実装しています：",
)
GO_OVERVIEW_ES = (
    "El SDK de Go se encuentra actualmente en una fase temprana de desarrollo (v0.5.0), pero implementa las características principales de Ring 1/Ring 2 de la especificación V2:",
    "El SDK de Go (v1.0.0) es la versión estable Wave-5 e implementa las características principales de Ring 1/Ring 2 de la especificación V2:",
)


def apply_replacements(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    for old, new in (GO_OVERVIEW_EN, GO_OVERVIEW_ZH, GO_OVERVIEW_JA, GO_OVERVIEW_ES):
        text = text.replace(old, new)
    # protocol contributing historical note — keep protocol v0.7.0 mention as historical
    return text


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in {".md", ".astro"}:
            continue
        original = read_text(path)
        updated = apply_replacements(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed += 1
            print(f"updated: {path.relative_to(ROOT.parent)}")
    print(f"done: {changed} files")


if __name__ == "__main__":
    main()
