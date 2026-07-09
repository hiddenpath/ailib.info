#!/usr/bin/env python3
"""Patch ailib.info rust landing pages and homepage cards."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUST_CARD_OLD = """              description="High-performance Rust runtime. ProviderDriver abstraction, MCP tool bridge, Computer Use safety, extended multimodal, and operator-based streaming pipeline."
              features={[
                'ProviderDriver (OpenAI/Anthropic/Gemini)',
                'MCP tool bridge with namespace isolation',
                'Computer Use + SafetyPolicy',
                'Extended multimodal validation',
                'Capability Registry (feature-gated)',
                'Operator-based streaming pipeline',
                '185+ tests, published on Crates.io',
              ]}"""

RUST_CARD_NEW = """              description="High-performance Rust runtime. E/P workspace (ai-lib-core + ai-lib-contact), manifest-driven Pipeline + AiClient, structured output, and feature-gated capability modules."
              features={[
                'AiClient + operator-based streaming pipeline',
                'ai-lib-core / ai-lib-contact workspace crates',
                '13 V2 standard error codes',
                'Structured output & text-tool (TTC)',
                'Optional: embeddings, MCP bridge, computer_use (feature-gated)',
                'Opt-in resilience (ai_lib_rust::resilience)',
                'Published on Crates.io v1.0.1',
              ]}"""

CODE_OLD_MARKER = '.user(<span style="color:#a5d6ff">"Explain AI-Protocol"</span>)'
CODE_NEW = """.messages(vec![Message::user(<span style="color:#a5d6ff">"Hello"</span>)])"""

for path in ROOT.glob("src/pages/**/index.astro"):
    text = path.read_bytes()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            content = text.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        content = text.decode("utf-8", errors="replace")

    changed = False
    if RUST_CARD_OLD in content:
        content = content.replace(RUST_CARD_OLD, RUST_CARD_NEW)
        changed = True
    if CODE_OLD_MARKER in content:
        content = content.replace(CODE_OLD_MARKER, CODE_NEW)
        content = content.replace(
            "StreamingEvent::ContentDelta {'{'} text, .. {'}'}",
            "StreamingEvent::PartialContentDelta {'{'} content, .. {'}'}",
        )
        content = content.replace(
            'print!(<span style="color:#a5d6ff">"{\'{\'}text{\'}\'}"</span>)',
            'print!(<span style="color:#a5d6ff">"{\'{\'}content{\'}\'}"</span>)',
        )
        content = content.replace(
            """StreamingEvent::StreamEnd {'{'} stats, .. {'}'}
            => println!(<span style="color:#a5d6ff">"\\nTokens: {'{'}{'}'}"</span>,
                stats.total_tokens),""",
            "StreamingEvent::StreamEnd {'{'} .. {'}'} => break,",
        )
        if "use futures::StreamExt" not in content and "execute_stream" in content:
            content = content.replace(
                "<span style=\"color:#ff7b72\">use</span> ai_lib_rust::{'{'}AiClient, Message, StreamingEvent{'}'};",
                "<span style=\"color:#ff7b72\">use</span> ai_lib_rust::{'{'}AiClient, Message, StreamingEvent{'}'};\n<span style=\"color:#ff7b72\">use</span> futures::StreamExt;",
            )
        changed = True

    if changed:
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"updated {path.relative_to(ROOT)}")

# Sync zh-cn overview/quickstart from en (site keeps en as canonical for now)
for name in ("overview.md", "quickstart.md", "resilience.md"):
    en = ROOT / f"src/content/docs/rust/{name}"
    zh = ROOT / f"src/content/docs/zh-cn/rust/{name}"
    if en.exists() and zh.exists():
        zh.write_text(en.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        print(f"synced zh-cn/rust/{name}")

print("done")
