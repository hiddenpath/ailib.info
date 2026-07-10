#!/usr/bin/env python3
"""Patch remaining untranslated strings on locale landing pages + meta."""

from __future__ import annotations

from pathlib import Path

PAGES = Path(__file__).resolve().parents[1] / "src" / "pages"

PATCHES = {
    "zh-cn": [
        ("content=\"ai-lib-go is the high-performance Go runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
         "content=\"ai-lib-go 是 AI-Protocol 的 Go 运行时。pkg/ailib 执行层 + pkg/contact 回退策略，协议优先 HTTP 与 ExecutionMetadata。\""),
        ("content=\"ai-lib-python is the official Python runtime for AI-Protocol. Async-first, Pydantic v2 types, production-grade telemetry, model routing.\"",
         "content=\"ai-lib-python 是 AI-Protocol 官方 Python 运行时。异步优先、Pydantic v2、清单 Pipeline + AiClient，韧性可选。\""),
        ("content=\"ai-lib-ts is the TypeScript/Node.js runtime for AI-Protocol. Protocol-driven, streaming-first, with Resilience, Routing, MCP, and Multimodal support.\"",
         "content=\"ai-lib-ts 是 AI-Protocol 的 TypeScript/Node.js 运行时。HttpTransport + 清单解析，/core 与 /contact 入口。\""),
        ("Protocol Loading", "协议加载"),
        ("""Loads provider manifests from local files, environment variables, or GitHub
                fallback. Supports hot-reload via file watching. Zero restart needed for config
                updates.""",
         """从本地文件、环境变量或 GitHub 回退加载服务商清单。
                支持文件监视热重载，配置更新无需重启。"""),
        ("Resilience Patterns", "韧性模式"),
        ("""Built-in circuit breaker, token bucket rate limiter, exponential backoff retry, and
                max-inflight backpressure. All configurable via environment variables.""",
         """内置熔断、令牌桶限流、指数退避重试与 max-inflight 背压。
                均可通过环境变量配置。"""),
        ("""The same code works across all providers. Switch from OpenAI to Anthropic to
                DeepSeek by changing one string —the protocol manifest handles the rest.""",
         """同一套代码适用于所有服务商。从 OpenAI 切换到 Anthropic 或 DeepSeek，
                只需改一个字符串——其余由协议清单处理。"""),
        ("""Full type hints with Pydantic v2 validation. ProtocolManifest, Message,
                ContentBlock, StreamingEvent —all type-safe with runtime validation.""",
         """完整类型注解与 Pydantic v2 校验。ProtocolManifest、Message、
                ContentBlock、StreamingEvent 均类型安全并带运行时验证。"""),
        ("""ModelManager with ModelArray for intelligent model selection. Strategies include
                round-robin, weighted, cost-based, and quality-based routing.""",
         """ModelManager + ModelArray 实现智能选型。策略含轮询、加权、成本优先与质量优先。"""),
        ("""MetricsCollector with Prometheus export. Distributed tracing via OpenTelemetry.
                Structured logging. Health monitoring. User feedback collection.""",
         """MetricsCollector 支持 Prometheus 导出。OpenTelemetry 分布式追踪。
                结构化日志、健康监控与用户反馈采集。"""),
        ("""JSON mode configuration, schema generation from Pydantic models, output validation.
                Guardrails with content filters and PII detection.""",
         """JSON 模式配置、由 Pydantic 模型生成 schema、输出校验。
                Guardrails 提供内容过滤与 PII 检测。"""),
        ("Protocol-driven architecture with type-safe execution, resilient by default, and fully\n              extensible.",
         "协议驱动架构：类型安全执行、默认可选韧性、完全可扩展。"),
    ],
    "ja": [
        ("content=\"ai-lib-go is the high-performance Go runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
         "content=\"AI-Protocol 向け Go ランタイム。pkg/ailib 実行層と pkg/contact フォールバック。\""),
        ("content=\"ai-lib-python is the official Python runtime for AI-Protocol. Async-first, Pydantic v2 types, production-grade telemetry, model routing.\"",
         "content=\"AI-Protocol 公式 Python ランタイム。非同期優先、Pydantic v2、マニフェスト Pipeline + AiClient。\""),
        ("content=\"ai-lib-ts is the TypeScript/Node.js runtime for AI-Protocol. Protocol-driven, streaming-first, with Resilience, Routing, MCP, and Multimodal support.\"",
         "content=\"AI-Protocol 向け TypeScript/Node.js ランタイム。HttpTransport + マニフェスト解析、/core と /contact。\""),
        ("Protocol Loading", "プロトコル読み込み"),
        ("""Loads provider manifests from local files, environment variables, or GitHub
                fallback. Supports hot-reload via file watching. Zero restart needed for config
                updates.""",
         """ローカル・環境変数・GitHub フォールバックからプロバイダーマニフェストを読み込み。
                ファイル監視によるホットリロード対応。再起動不要。"""),
        ("Resilience Patterns", "レジリエンスパターン"),
        ("""Built-in circuit breaker, token bucket rate limiter, exponential backoff retry, and
                max-inflight backpressure. All configurable via environment variables.""",
         """組み込みサーキットブレーカー、トークンバケット制限、指数バックオフ再試行、
                max-inflight 背圧。環境変数で設定可能。"""),
        ("""The same code works across all providers. Switch from OpenAI to Anthropic to
                DeepSeek by changing one string —the protocol manifest handles the rest.""",
         """同じコードがすべてのプロバイダーで動作します。OpenAI から Anthropic、DeepSeek へは
                文字列を一つ変えるだけ——残りはマニフェストが処理します。"""),
        ("""Full type hints with Pydantic v2 validation. ProtocolManifest, Message,
                ContentBlock, StreamingEvent —all type-safe with runtime validation.""",
         """Pydantic v2 による完全な型ヒントと検証。ProtocolManifest、Message、
                ContentBlock、StreamingEvent は実行時検証付きで型安全。"""),
        ("""ModelManager with ModelArray for intelligent model selection. Strategies include
                round-robin, weighted, cost-based, and quality-based routing.""",
         """ModelManager + ModelArray による知的モデル選択。ラウンドロビン、加重、コスト、品質戦略。"""),
        ("""MetricsCollector with Prometheus export. Distributed tracing via OpenTelemetry.
                Structured logging. Health monitoring. User feedback collection.""",
         """Prometheus 出力対応 MetricsCollector。OpenTelemetry 分散トレーシング。
                構造化ログ、ヘルス監視、フィードバック収集。"""),
        ("""JSON mode configuration, schema generation from Pydantic models, output validation.
                Guardrails with content filters and PII detection.""",
         """JSON モード設定、Pydantic モデルからの schema 生成、出力検証。
                コンテンツフィルタと PII 検出の Guardrails。"""),
        ("Protocol-driven architecture with type-safe execution, resilient by default, and fully\n              extensible.",
         "プロトコル駆動アーキテクチャ：型安全な実行、既定のレジリエンス、完全な拡張性。"),
    ],
    "es": [
        ("content=\"ai-lib-go is the high-performance Go runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
         "content=\"Runtime Go para AI-Protocol. pkg/ailib + pkg/contact, HTTP por manifiestos y ExecutionMetadata.\""),
        ("content=\"ai-lib-python is the official Python runtime for AI-Protocol. Async-first, Pydantic v2 types, production-grade telemetry, model routing.\"",
         "content=\"Runtime Python oficial para AI-Protocol. Async-first, Pydantic v2, Pipeline + AiClient por manifiestos.\""),
        ("content=\"ai-lib-ts is the TypeScript/Node.js runtime for AI-Protocol. Protocol-driven, streaming-first, with Resilience, Routing, MCP, and Multimodal support.\"",
         "content=\"Runtime TypeScript/Node.js para AI-Protocol. HttpTransport + parsers de manifiesto, entradas /core y /contact.\""),
        ("Protocol Loading", "Carga de protocolo"),
        ("""Loads provider manifests from local files, environment variables, or GitHub
                fallback. Supports hot-reload via file watching. Zero restart needed for config
                updates.""",
         """Carga manifiestos desde archivos locales, variables de entorno o GitHub.
                Hot-reload por vigilancia de archivos. Sin reinicio para actualizar la config."""),
        ("Resilience Patterns", "Patrones de resiliencia"),
        ("""Built-in circuit breaker, token bucket rate limiter, exponential backoff retry, and
                max-inflight backpressure. All configurable via environment variables.""",
         """Circuit breaker, limitador token bucket, reintentos con backoff exponencial y
                backpressure max-inflight. Configurable por variables de entorno."""),
        ("""The same code works across all providers. Switch from OpenAI to Anthropic to
                DeepSeek by changing one string —the protocol manifest handles the rest.""",
         """El mismo código funciona con todos los proveedores. Cambia de OpenAI a Anthropic o
                DeepSeek con un solo string: el manifiesto gestiona el resto."""),
        ("""Full type hints with Pydantic v2 validation. ProtocolManifest, Message,
                ContentBlock, StreamingEvent —all type-safe with runtime validation.""",
         """Tipado completo con validación Pydantic v2. ProtocolManifest, Message,
                ContentBlock y StreamingEvent son type-safe con validación en runtime."""),
        ("""ModelManager with ModelArray for intelligent model selection. Strategies include
                round-robin, weighted, cost-based, and quality-based routing.""",
         """ModelManager + ModelArray para selección inteligente. Estrategias: round-robin,
                ponderada, por coste y por calidad."""),
        ("""MetricsCollector with Prometheus export. Distributed tracing via OpenTelemetry.
                Structured logging. Health monitoring. User feedback collection.""",
         """MetricsCollector con exportación Prometheus. Trazas OpenTelemetry.
                Logging estructurado, salud y feedback de usuario."""),
        ("""JSON mode configuration, schema generation from Pydantic models, output validation.
                Guardrails with content filters and PII detection.""",
         """Modo JSON, generación de schema desde modelos Pydantic y validación de salida.
                Guardrails con filtros de contenido y detección de PII."""),
        ("Protocol-driven architecture with type-safe execution, resilient by default, and fully\n              extensible.",
         "Arquitectura orientada a protocolo: ejecución tipada, resiliencia opcional y extensibilidad total."),
    ],
}


def main() -> None:
    for locale, pairs in PATCHES.items():
        for path in (PAGES / locale).rglob("*.astro"):
            text = path.read_text(encoding="utf-8")
            orig = text
            for old, new in pairs:
                text = text.replace(old, new)
            if text != orig:
                path.write_text(text, encoding="utf-8", newline="\n")
                print(f"patched {path.relative_to(PAGES.parent.parent)}")
    print("done")


if __name__ == "__main__":
    main()
