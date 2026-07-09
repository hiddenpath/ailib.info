#!/usr/bin/env python3
"""Patch ailib.info python landing pages and homepage cards."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PYTHON_CARD_OLD = """              description="Developer-friendly Python runtime. ProviderDriver abstraction, MCP tool bridge, Computer Use safety, extended multimodal, STT/TTS/Rerank extras."
              features={[
                'ProviderDriver (OpenAI/Anthropic/Gemini)',
                'MCP tool bridge with namespace isolation',
                'Computer Use + SafetyPolicy',
                'STT / TTS / Rerank extras',
                'Capability Registry (pip extras)',
                'Pydantic v2 + full async/await',
                '75+ V2 tests, published on PyPI',
              ]}"""

PYTHON_CARD_NEW = """              description="Async Python runtime. E/P module separation, manifest-driven Pipeline + AiClient, Pydantic v2 types, and pip-extra capability modules."
              features={[
                'AiClient + operator-based streaming pipeline',
                'Fluent chat builder (.messages / .user / .stream)',
                '13 V2 standard error codes',
                'Structured output & text-tool types',
                'Optional: embeddings, MCP bridge, computer_use (pip extras)',
                'Opt-in resilience (production_ready / resilience module)',
                'Published on PyPI v1.0.0',
              ]}"""

PYTHON_HERO_OLD = """              Developer-friendly, protocol-driven AI client. V2 standard error codes (13 codes),
              capability-based extras (8 extras + full), full async support, Pydantic v2 type
              safety, production-grade telemetry, and smart model routing. Python 3.10+."""

PYTHON_HERO_NEW = """              Async, protocol-driven AI client (v1.0.0). Default path: manifest → Pipeline →
              httpx transport. Pydantic v2 types, 13 V2 error codes, pip extras for capabilities,
              and opt-in resilience via AiClientBuilder. Python 3.10+."""

PYTHON_FEATURES_REPLACEMENTS = [
    (
        """              <h3 class="font-bold text-[var(--text)] mb-2">Model Routing</h3>
              <p class="text-sm text-[var(--text-dim)]">
                ModelManager with ModelArray for intelligent model selection. Strategies include
                round-robin, weighted, cost-based, and quality-based routing.
              </p>""",
        """              <h3 class="font-bold text-[var(--text)] mb-2">Manifest Pipeline</h3>
              <p class="text-sm text-[var(--text-dim)]">
                Operator pipeline (Decoder → Selector → Accumulator → EventMapper) built from
                provider manifests. Same protocol path as other AI-Lib runtimes.
              </p>""",
    ),
    (
        """              <h3 class="font-bold text-[var(--text)] mb-2">Production Telemetry</h3>
              <p class="text-sm text-[var(--text-dim)]">
                MetricsCollector with Prometheus export. Distributed tracing via OpenTelemetry.
                Structured logging. Health monitoring. User feedback collection.
              </p>""",
        """              <h3 class="font-bold text-[var(--text)] mb-2">Opt-in Telemetry</h3>
              <p class="text-sm text-[var(--text-dim)]">
                OpenTelemetry integration via pip extra <code>telemetry</code>. Feedback reporting
                through ai_lib_python.telemetry — not enabled by AiClient.create() alone.
              </p>""",
    ),
]


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


for path in ROOT.glob("src/pages/**/index.astro"):
    content = read_text(path)
    changed = False

    if PYTHON_CARD_OLD in content:
        content = content.replace(PYTHON_CARD_OLD, PYTHON_CARD_NEW)
        changed = True

  # zh-cn card may differ slightly — patch common overclaim block
    zh_old = "ProviderDriver 抽象、MCP 工具桥"
    if zh_old in content and PYTHON_CARD_NEW not in content:
        content = content.replace(
            """              description="开发者友好的 Python 运行时。ProviderDriver 抽象、MCP 工具桥、Computer Use 安全策略、扩展多模态、STT/TTS/Rerank 扩展。"
              features={[
                'ProviderDriver（OpenAI/Anthropic/Gemini）',
                'MCP 工具桥 + 命名空间隔离',
                'Computer Use + SafetyPolicy',
                '扩展多模态校验',
                'Capability Registry（pip extras）',
                'Async 优先 + Pydantic v2 类型',
                'PyPI v1.0.0',
              ]}""",
            """              description="异步 Python 运行时。E/P 模块分层、清单驱动 Pipeline + AiClient、Pydantic v2 类型与 pip extras 能力模块。"
              features={[
                'AiClient + 算子流式 Pipeline',
                '流式 chat builder（.messages / .user / .stream）',
                '13 个 V2 标准错误码',
                '结构化输出与 text-tool 类型',
                '可选：embeddings、MCP 桥接、computer_use（pip extras）',
                '可选 resilience（production_ready）',
                'PyPI v1.0.0',
              ]}""",
        )
        changed = True

    if PYTHON_HERO_OLD in content:
        content = content.replace(PYTHON_HERO_OLD, PYTHON_HERO_NEW)
        changed = True

    if "/python/index.astro" in str(path).replace("\\", "/"):
        for old, new in PYTHON_FEATURES_REPLACEMENTS:
            if old in content:
                content = content.replace(old, new)
                changed = True

    if changed:
        write_text(path, content)
        print(f"updated {path.relative_to(ROOT)}")

# Sync zh-cn docs from en
for name in ("overview.md", "quickstart.md", "resilience.md"):
    en = ROOT / f"src/content/docs/python/{name}"
    zh = ROOT / f"src/content/docs/zh-cn/python/{name}"
  # zh-cn gets same technical content for now (DOC-001 site docs)
    shutil.copy2(en, zh)
    print(f"synced zh-cn {name}")

print("done")
