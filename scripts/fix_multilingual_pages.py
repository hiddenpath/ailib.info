#!/usr/bin/env python3
"""Fix encoding corruption and regenerate locale runtime landing pages from EN templates."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "src" / "pages"

# Spanish / punctuation mojibake (UTF-8 read as Latin-1)
ES_CHAR_FIXES = [
    ("compilaciÃ³n", "compilación"),
    ("cÃ³digo", "código"),
    ("cÃ³digos", "códigos"),
    ("estÃ¡ndar", "estándar"),
    ("estÃ¡ndar", "estándar"),
    ("caracterÃ­sticas", "características"),
    ("caracterÃ­stica", "característica"),
    ("lÃ³gica", "lógica"),
    ("especificaciÃ³n", "especificación"),
    ("especificaciÃ³n", "especificación"),
    ("pirÃ¡mide", "pirámide"),
    ("validaciÃ³n", "validación"),
    ("ValidaciÃ³n", "Validación"),
    ("configuraciÃ³n", "configuración"),
    ("ConfiguraciÃ³n", "Configuración"),
    ("telemetrÃ­a", "telemetría"),
    ("TelemetrÃ­a", "Telemetría"),
    ("mÃ¡quina", "máquina"),
    ("mÃºltiples", "múltiples"),
    ("mÃ³dulos", "módulos"),
    ("bÃ¡sicos", "básicos"),
    ("Ã­ndice", "índice"),
    ("Ãºnico", "único"),
    ("Ã¡rea", "área"),
    ("Ã©xito", "éxito"),
    ("pÃºblico", "público"),
    ("Ã³", "ó"),
    ("Ã¡", "á"),
    ("Ã©", "é"),
    ("Ã­", "í"),
    ("Ãº", "ú"),
    ("Ã±", "ñ"),
    ("Ã¼", "ü"),
    ("â€”", "—"),
    ("â€?", "—"),
    ("â†?", "→"),
    ("Â ", " "),
]

EN_PUNCT_FIXES = [
    ("â€?", "—"),
    ("â†?", "→"),
    ("manifest ? Pipeline ?", "manifest → Pipeline →"),
]


def fix_es_text(text: str) -> str:
    for old, new in ES_CHAR_FIXES:
        text = text.replace(old, new)
    return text


def fix_en_text(text: str) -> str:
    for old, new in EN_PUNCT_FIXES:
        text = text.replace(old, new)
    return text


def read_text_safe(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def read_en(runtime: str) -> str:
    return read_text_safe(PAGES / runtime / "index.astro")


def write_utf8(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)}")


def base_localize(en: str, *, locale: str, lang: str, import_depth: str, url_prefix: str) -> str:
    out = en
    out = out.replace("const locale = 'en'", f"const locale = '{locale}'")
    out = out.replace('<html lang="en"', f'<html lang="{lang}"')
    for segment in ("styles/", "components/"):
        out = out.replace(f"'../../{segment}", f"'{import_depth}{segment}")
    # docs and landing links
    for segment in ("rust", "ts", "python", "go", "protocol", "quickstart", "ecosystem", "intro"):
        out = out.replace(f'href="/{segment}/', f'href="{url_prefix}/{segment}/')
    out = fix_en_text(out)
    return out


# --- zh-CN strings per runtime (code-first, aligned with AILIB-005) ---

ZH_CN_COMMON = [
    (">Start Building with Rust</h2>", ">开始使用 Rust 构建</h2>"),
    (">Start Building with Python</h2>", ">开始使用 Python 构建</h2>"),
    (">Start Building with Go</h2>", ">开始使用 Go 构建</h2>"),
    (">Full Documentation</a", ">完整文档</a"),
]

ZH_CN = {
    "rust": [
        ("ai-lib-rust | High-Performance Rust Runtime for AI-Protocol",
         "ai-lib-rust | AI-Protocol 高性能 Rust 运行时"),
        ("content=\"ai-lib-rust is the high-performance Rust runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
         "content=\"ai-lib-rust 是 AI-Protocol 的高性能 Rust 运行时。清单驱动的 Pipeline + AiClient，E/P 工作区，可编译示例与 feature 门控能力模块。\""),
        ("<span class=\"gradient-text-rust\">Rust Runtime</span>", "<span class=\"gradient-text-rust\">Rust 运行时</span>"),
        ("<span class=\"text-[var(--text)]\">for AI-Protocol.</span>", "<span class=\"text-[var(--text)]\">适用于 AI-Protocol。</span>"),
        ("""High-performance Rust runtime for AI-Protocol. Manifest-driven
              <code>Pipeline</code> + <code>AiClient</code>, E/P workspace
              (<code>ai-lib-core</code> + <code>ai-lib-contact</code>), 13 V2 error codes,
              and feature-gated capability modules.""",
         """AI-Protocol 高性能 Rust 运行时（v1.0.1）。默认路径：清单 → Pipeline → HttpTransport。
              E/P 工作区（<code>ai-lib-core</code> + <code>ai-lib-contact</code>），13 个 V2 标准错误码，
              以及 feature 门控的能力模块。"""),
        (">Quick Start</a", ">快速开始</a"),
        (">Key Features</h2>", ">核心特性</h2>"),
        (">Simple, Unified API</h2>", ">统一、简洁的 API</h2>"),
        (">Internal Architecture</h2>", ">内部架构</h2>"),
        (">Module Overview</h2>", ">模块概览</h2>"),
        (">Start Building with Rust</h2>", ">开始使用 Rust 构建</h2>"),
        (">Start Building with Python</h2>", ">开始使用 Python 构建</h2>"),
        (">Start Building with Go</h2>", ">开始使用 Go 构建</h2>"),
        (">Full Documentation</a", ">完整文档</a"),
        ("Built-in <code>max_inflight</code> backpressure on <code>AiClient</code>. Retry,\n                rate limit, and circuit breaker live in <code>ai_lib_rust::resilience</code> — opt-in.",
         "内置 <code>max_inflight</code> 背压；重试、限流与熔断在 <code>ai_lib_rust::resilience</code> 中，需显式启用。"),
    ],
    "ts": [
        ("ai-lib-ts | TypeScript/Node.js Runtime for AI-Protocol",
         "ai-lib-ts | AI-Protocol TypeScript/Node.js 运行时"),
        ("content=\"ai-lib-ts is the TypeScript/Node.js runtime for AI-Protocol. Protocol-driven, streaming-first, with Resilience, Routing, MCP, and Multimodal support.\"",
         "content=\"ai-lib-ts 是 AI-Protocol 的 TypeScript/Node.js 运行时。HttpTransport + 清单解析，/core 与 /contact 入口，策略层可选。\""),
        ("<span class=\"gradient-text\">TypeScript Runtime</span>", "<span class=\"gradient-text\">TypeScript 运行时</span>"),
        ("<span class=\"text-[var(--text)]\">for AI-Protocol.</span>", "<span class=\"text-[var(--text)]\">适用于 AI-Protocol。</span>"),
        ("""Protocol-driven, streaming-first TypeScript/Node.js runtime. V2 manifest parsing,
              standard error codes, Resilience patterns, Model routing, MCP bridge, and multimodal
              support.""",
         """协议驱动的 TypeScript/Node.js 运行时（v1.0.0）。默认聊天路径为 HttpTransport + 清单解析（非 Pipeline 算子路径）。
              提供 /core（执行层）与 /contact（策略层）入口，13 个 V2 错误码。"""),
        (">Quick Start</a", ">快速开始</a"),
        (">Key Features</h2>", ">核心特性</h2>"),
        (">Documentation</h2>", ">文档</h2>"),
        (">Get up and running in minutes.</p>", ">几分钟内上手。</p>"),
        (">Complete API reference.</p>", ">完整 API 参考。</p>"),
        (">Real-time response handling.</p>", ">实时流式响应处理。</p>"),
        (">Production-ready patterns.</p>", ">生产级韧性模式（可选配置）。</p>"),
        (">Architecture and concepts.</p>", ">架构与核心概念。</p>"),
        ("Quick Start →", "快速开始 →"),
        ("AiClient API →", "AiClient API →"),
        ("Streaming →", "流式处理 →"),
        ("Resilience →", "韧性模式 →"),
        ("Advanced →", "高级特性 →"),
        ("Overview →", "概述 →"),
    ],
    "python": [
        ("ai-lib-python | Python Runtime for AI-Protocol",
         "ai-lib-python | AI-Protocol Python 运行时"),
        ("content=\"ai-lib-python is the official Python runtime for AI-Protocol. Async-first, Pydantic v2 types, production-grade telemetry, model routing.\"",
         "content=\"ai-lib-python 是 AI-Protocol 官方 Python 运行时。异步优先、Pydantic v2 类型、清单 Pipeline + AiClient，韧性模块可选。\""),
        ("<span class=\"gradient-text-python\">Python Runtime</span>", "<span class=\"gradient-text-python\">Python 运行时</span>"),
        ("<span class=\"text-[var(--text)]\">for AI-Protocol.</span>", "<span class=\"text-[var(--text)]\">适用于 AI-Protocol。</span>"),
        ("""Async, protocol-driven AI client (v1.0.0). Default path: manifest → Pipeline →
              httpx transport. Pydantic v2 types, 13 V2 error codes, pip extras for capabilities,
              and opt-in resilience via AiClientBuilder. Python 3.10+.""",
         """异步、协议驱动的 AI 客户端（v1.0.0）。默认路径：清单 → Pipeline → httpx 传输。
              Pydantic v2 类型、13 个 V2 错误码、pip extras 能力模块，以及通过 AiClientBuilder 可选启用的 resilience。Python 3.10+。"""),
        (">Quick Start</a", ">快速开始</a"),
        (">Key Features</h2>", ">核心特性</h2>"),
    ],
    "go": [
        ("ai-lib-go | High-Performance Go Runtime for AI-Protocol",
         "ai-lib-go | AI-Protocol Go 运行时"),
        ("content=\"ai-lib-go is the high-performance Go runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
         "content=\"ai-lib-go 是 AI-Protocol 的 Go 运行时。pkg/ailib 执行层 + pkg/contact 回退策略，协议优先 HTTP 与 ExecutionMetadata。\""),
        ("<span class=\"gradient-text-rust\">Go Runtime</span>", "<span class=\"gradient-text-rust\">Go 运行时</span>"),
        ("<span class=\"text-[var(--text)]\">for AI-Protocol.</span>", "<span class=\"text-[var(--text)]\">适用于 AI-Protocol。</span>"),
        ("""High-performance, protocol-driven AI client. V2 standard error codes (13 codes),
              feature flags (7 features + full meta-feature), zero hardcoded provider logic,
              operator-based streaming pipeline, compile-time type safety, and sub-millisecond
              overhead.""",
         """Go 协议运行时（v1.0.0）。pkg/ailib 负责清单 HTTP 聊天；pkg/contact 提供熔断与多提供商回退。
              13 个 V2 标准错误码，ChatStream 默认 openai_sse 解码器。Go 1.21+。"""),
        (">Quick Start</a", ">快速开始</a"),
        (">Key Features</h2>", ">核心特性</h2>"),
    ],
}

JA_COMMON = [
    (">Start Building with Rust</h2>", ">Rust で構築を始める</h2>"),
    (">Start Building with Python</h2>", ">Python で構築を始める</h2>"),
    (">Start Building with Go</h2>", ">Go で構築を始める</h2>"),
    (">Full Documentation</a", ">完全なドキュメント</a"),
]

ES_COMMON = [
    (">Start Building with Rust</h2>", ">Empieza a construir con Rust</h2>"),
    (">Start Building with Python</h2>", ">Empieza a construir con Python</h2>"),
    (">Start Building with Go</h2>", ">Empieza a construir con Go</h2>"),
    (">Full Documentation</a", ">Documentación completa</a"),
]

JA = {
    "rust": [
        ("ai-lib-rust | High-Performance Rust Runtime for AI-Protocol",
         "ai-lib-rust | AI-Protocol 高性能 Rust ランタイム"),
        ("content=\"ai-lib-rust is the high-performance Rust runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
         "content=\"AI-Protocol 向け高性能 Rust ランタイム。マニフェスト駆動 Pipeline + AiClient、E/P ワークスペース、feature ゲート付き能力モジュール。\""),
        ("<span class=\"gradient-text-rust\">Rust Runtime</span>", "<span class=\"gradient-text-rust\">Rust ランタイム</span>"),
        ("<span class=\"text-[var(--text)]\">for AI-Protocol.</span>", "<span class=\"text-[var(--text)]\">for AI-Protocol。</span>"),
        (">Quick Start</a", ">クイックスタート</a"),
        (">Key Features</h2>", ">主な機能</h2>"),
        ("""High-performance Rust runtime for AI-Protocol. Manifest-driven
              <code>Pipeline</code> + <code>AiClient</code>, E/P workspace
              (<code>ai-lib-core</code> + <code>ai-lib-contact</code>), 13 V2 error codes,
              and feature-gated capability modules.""",
         """AI-Protocol 向け高性能 Rust ランタイム（v1.0.1）。マニフェスト → Pipeline → HttpTransport。
              E/P ワークスペース（ai-lib-core + ai-lib-contact）、V2 標準エラーコード 13 種、feature ゲート付き能力モジュール。"""),
    ],
    "ts": [
        ("ai-lib-ts | TypeScript/Node.js Runtime for AI-Protocol",
         "ai-lib-ts | AI-Protocol TypeScript/Node.js ランタイム"),
        ("<span class=\"gradient-text\">TypeScript Runtime</span>", "<span class=\"gradient-text\">TypeScript ランタイム</span>"),
        (">Quick Start</a", ">クイックスタート</a"),
        (">Key Features</h2>", ">主な機能</h2>"),
        ("""Protocol-driven, streaming-first TypeScript/Node.js runtime. V2 manifest parsing,
              standard error codes, Resilience patterns, Model routing, MCP bridge, and multimodal
              support.""",
         """プロトコル駆動の TypeScript/Node.js ランタイム（v1.0.0）。既定のチャット経路は HttpTransport + マニフェスト解析。
              /core と /contact エントリポイント、V2 標準エラーコード 13 種。"""),
    ],
    "python": [
        ("ai-lib-python | Python Runtime for AI-Protocol",
         "ai-lib-python | AI-Protocol Python ランタイム"),
        ("<span class=\"gradient-text-python\">Python Runtime</span>", "<span class=\"gradient-text-python\">Python ランタイム</span>"),
        (">Quick Start</a", ">クイックスタート</a"),
        ("""Async, protocol-driven AI client (v1.0.0). Default path: manifest → Pipeline →
              httpx transport. Pydantic v2 types, 13 V2 error codes, pip extras for capabilities,
              and opt-in resilience via AiClientBuilder. Python 3.10+.""",
         """非同期のプロトコル駆動 AI クライアント（v1.0.0）。既定経路：マニフェスト → Pipeline → httpx。
              Pydantic v2 型、V2 エラーコード 13 種、pip extras、AiClientBuilder によるオプトイン resilience。Python 3.10+。"""),
    ],
    "go": [
        ("ai-lib-go | High-Performance Go Runtime for AI-Protocol",
         "ai-lib-go | AI-Protocol Go ランタイム"),
        ("<span class=\"gradient-text-rust\">Go Runtime</span>", "<span class=\"gradient-text-rust\">Go ランタイム</span>"),
        (">Quick Start</a", ">クイックスタート</a"),
        ("""High-performance, protocol-driven AI client. V2 standard error codes (13 codes),
              feature flags (7 features + full meta-feature), zero hardcoded provider logic,
              operator-based streaming pipeline, compile-time type safety, and sub-millisecond
              overhead.""",
         """Go プロトコルランタイム（v1.0.0）。pkg/ailib 実行層と pkg/contact フォールバック。プロトコル優先 HTTP と ExecutionMetadata。Go 1.21+。"""),
    ],
}

ES = {
    "rust": [
        ("ai-lib-rust | High-Performance Rust Runtime for AI-Protocol",
         "ai-lib-rust | Runtime Rust de alto rendimiento para AI-Protocol"),
        ("content=\"ai-lib-rust is the high-performance Rust runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
         "content=\"Runtime Rust de alto rendimiento para AI-Protocol. Pipeline + AiClient basados en manifiestos, workspace E/P y módulos de capacidad con features.\""),
        (">Quick Start</a", ">Inicio rápido</a"),
        (">Key Features</h2>", ">Características clave</h2>"),
        ("""High-performance Rust runtime for AI-Protocol. Manifest-driven
              <code>Pipeline</code> + <code>AiClient</code>, E/P workspace
              (<code>ai-lib-core</code> + <code>ai-lib-contact</code>), 13 V2 error codes,
              and feature-gated capability modules.""",
         """Runtime Rust de alto rendimiento para AI-Protocol (v1.0.1). Ruta predeterminada: manifiesto → Pipeline → HttpTransport.
              Workspace E/P (ai-lib-core + ai-lib-contact), 13 códigos de error V2 y módulos de capacidad con features."""),
    ],
    "ts": [
        (">Quick Start</a", ">Inicio rápido</a"),
        (">Key Features</h2>", ">Características clave</h2>"),
        (">Documentation</h2>", ">Documentación</h2>"),
        ("""Protocol-driven, streaming-first TypeScript/Node.js runtime. V2 manifest parsing,
              standard error codes, Resilience patterns, Model routing, MCP bridge, and multimodal
              support.""",
         """Runtime TypeScript/Node.js orientado a protocolo (v1.0.0). Ruta de chat: HttpTransport + parsers de manifiesto.
              Puntos de entrada /core y /contact, 13 códigos de error V2."""),
    ],
    "python": [
        (">Quick Start</a", ">Inicio rápido</a"),
        (">Key Features</h2>", ">Características clave</h2>"),
        ("""Async, protocol-driven AI client (v1.0.0). Default path: manifest → Pipeline →
              httpx transport. Pydantic v2 types, 13 V2 error codes, pip extras for capabilities,
              and opt-in resilience via AiClientBuilder. Python 3.10+.""",
         """Cliente AI asíncrono orientado a protocolo (v1.0.0). Ruta: manifiesto → Pipeline → httpx.
              Tipos Pydantic v2, 13 códigos de error V2, extras pip y resiliencia opt-in vía AiClientBuilder. Python 3.10+."""),
    ],
    "go": [
        (">Quick Start</a", ">Inicio rápido</a"),
        (">Key Features</h2>", ">Características clave</h2>"),
        ("""High-performance, protocol-driven AI client. V2 standard error codes (13 codes),
              feature flags (7 features + full meta-feature), zero hardcoded provider logic,
              operator-based streaming pipeline, compile-time type safety, and sub-millisecond
              overhead.""",
         """Runtime Go orientado a protocolo (v1.0.0). pkg/ailib + pkg/contact, HTTP basado en manifiestos y ExecutionMetadata. Go 1.21+."""),
    ],
}


def apply_replacements(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def regenerate_locale(locale: str, lang: str, import_depth: str, url_prefix: str, runtime_map: dict) -> None:
    for runtime, pairs in runtime_map.items():
        en = read_en(runtime)
        out = base_localize(
            en,
            locale=locale,
            lang=lang,
            import_depth=import_depth,
            url_prefix=url_prefix,
        )
        out = apply_replacements(out, pairs)
        if locale == "zh-cn":
            out = apply_replacements(out, ZH_CN_COMMON)
        if locale == "ja":
            out = apply_replacements(out, JA_COMMON)
        if locale == "es":
            out = apply_replacements(out, ES_COMMON)
            out = fix_es_text(out)
        dest = PAGES / locale / runtime / "index.astro"
        write_utf8(dest, out)


def fix_es_index() -> None:
    path = PAGES / "es" / "index.astro"
    text = fix_es_text(read_text_safe(path))
    # sync project cards with en (code-first)
    text = text.replace(
        """description="Runtime Python amigable para desarrolladores. Códigos de error estándar V2, extras por capacidad, soporte async completo, tipos Pydantic v2 y telemetría de producción."
              features={[
                'ProviderDriver (OpenAI/Anthropic/Gemini)',
                'MCP tool bridge + aislamiento de namespace',
                'Computer Use + SafetyPolicy',
                'Extras STT/TTS/Rerank',
                'Seguridad de tipos Pydantic v2',
                'Enrutamiento y balanceo de carga de modelos',
                '75+ tests V2, publicado en PyPI',
              ]}""",
        """description="Runtime Python asíncrono. Separación E/P, Pipeline + AiClient basados en manifiestos, tipos Pydantic v2 y extras pip."
              features={[
                'AiClient + pipeline de streaming por operadores',
                'Builder fluido (.messages / .user / .stream)',
                '13 códigos de error estándar V2',
                'Salida estructurada y tipos text-tool',
                'Opcional: embeddings, puente MCP, computer_use (pip extras)',
                'Resiliencia opt-in (production_ready)',
                'Publicado en PyPI v1.0.0',
              ]}""",
    )
    text = text.replace(
        """description="Runtime TypeScript/Node.js para el ecosistema npm. Impulsado por protocolo, streaming-first, con Resilience, Routing, MCP y soporte multimodal."
              features={[
                'Parsing de manifiestos V2 + códigos de error estándar',
                'Resilience (Retry, CircuitBreaker, RateLimiter, Backpressure)',
                'ModelManager + CostBasedSelector + FallbackChain',
                'SttClient, TtsClient, RerankerClient',
                'McpToolBridge, EmbeddingClient, Plugins',
                'BatchExecutor + PreflightChecker',
                'fetch nativo, publicado en npm',
              ]}""",
        """description="Runtime TypeScript para npm. HttpTransport + parsers de manifiesto, entradas /core y /contact, capa de política opcional."
              features={[
                'AiClient + chat HTTP basado en manifiestos',
                'Entradas /core (E) y /contact (P)',
                '13 códigos de error estándar V2',
                'StreamingEvent con event_type',
                'Opcional: EmbeddingClient, McpToolBridge (solo formato)',
                'Reintento en transporte por defecto; CB/RL opt-in',
                'Publicado en npm v1.0.0',
              ]}""",
    )
    write_utf8(path, text)


def fix_en_pages() -> None:
    for runtime in ("rust", "ts", "python"):
        path = PAGES / runtime / "index.astro"
        write_utf8(path, fix_en_text(read_text_safe(path)))


def main() -> None:
    regenerate_locale("zh-cn", "zh-CN", "../../../", "/zh-cn", ZH_CN)
    regenerate_locale("ja", "ja", "../../../", "/ja", JA)
    regenerate_locale("es", "es", "../../../", "/es", ES)
    fix_en_pages()
    fix_es_index()
    print("done")


if __name__ == "__main__":
    main()
