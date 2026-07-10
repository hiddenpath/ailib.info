#!/usr/bin/env python3
"""Translate remaining Python landing-page module/architecture prose."""

from __future__ import annotations

from pathlib import Path

PAGES = Path(__file__).resolve().parents[1] / "src" / "pages"

PY = {
    "zh-cn": [
        ("""Same layered architecture as the Rust runtime —protocol-driven, operator-based,
              resilient by default.""",
         """与 Rust 运行时相同的分层架构——协议驱动、基于算子，韧性按需启用。"""),
        ("""ProtocolLoader (local/env/GitHub), Pydantic manifest models, JSON Schema validator,
                hot-reload support.""",
         """ProtocolLoader（本地 / 环境变量 / GitHub）、Pydantic 清单模型、JSON Schema 校验器、
                热重载支持。"""),
        ("""Decoder (SSE, JSON Lines, Anthropic SSE), Selector (JSONPath), Accumulator, FanOut,
                EventMapper (protocol-driven, default, Anthropic).""",
         """Decoder（SSE、JSON Lines、Anthropic SSE）、Selector（JSONPath）、Accumulator、FanOut、
                EventMapper（协议驱动 / 默认 / Anthropic）。"""),
        ("""ModelManager, ModelArray, selection strategies (round-robin, weighted, cost-based,
                quality-based). Pre-configured catalogs for major providers.""",
         """ModelManager、ModelArray 与选型策略（轮询、加权、成本、质量）。
                主流服务商预置目录。"""),
        ("""MetricsCollector (Prometheus), Tracer (OpenTelemetry), structured Logger,
                HealthChecker, user feedback collection.""",
         """MetricsCollector（Prometheus）、Tracer（OpenTelemetry）、结构化 Logger、
                HealthChecker、用户反馈采集。"""),
        ("""EmbeddingClient with vector operations. TokenCounter (tiktoken integration) and cost
                estimation for usage tracking.""",
         """EmbeddingClient 提供向量运算。TokenCounter（tiktoken 集成）与用量成本估算。"""),
        ("""EmbeddingClient 提供向量运算. TokenCounter (tiktoken integration) and cost
                estimation for usage tracking.""",
         """EmbeddingClient 提供向量运算。TokenCounter（tiktoken 集成）与用量成本估算。"""),
        ("""Plugin base class, PluginRegistry, HookManager, middleware chain. JSON mode config,
                SchemaGenerator, OutputValidator.""",
         """Plugin 基类、PluginRegistry、HookManager 与中间件链。JSON 模式配置、
                SchemaGenerator、OutputValidator。"""),
    ],
    "ja": [
        ("""Same layered architecture as the Rust runtime —protocol-driven, operator-based,
              resilient by default.""",
         """Rust ランタイムと同じ層構造——プロトコル駆動・オペレーターベース、レジリエンスはオプトイン。"""),
        ("""ProtocolLoader (local/env/GitHub), Pydantic manifest models, JSON Schema validator,
                hot-reload support.""",
         """ProtocolLoader（ローカル / 環境変数 / GitHub）、Pydantic マニフェストモデル、JSON Schema 検証、
                ホットリロード。"""),
        ("""Decoder (SSE, JSON Lines, Anthropic SSE), Selector (JSONPath), Accumulator, FanOut,
                EventMapper (protocol-driven, default, Anthropic).""",
         """Decoder（SSE、JSON Lines、Anthropic SSE）、Selector（JSONPath）、Accumulator、FanOut、
                EventMapper（プロトコル駆動 / デフォルト / Anthropic）。"""),
        ("""ModelManager, ModelArray, selection strategies (round-robin, weighted, cost-based,
                quality-based). Pre-configured catalogs for major providers.""",
         """ModelManager、ModelArray、選択戦略（ラウンドロビン、加重、コスト、品質）。
                主要プロバイダーの事前設定カタログ。"""),
        ("""MetricsCollector (Prometheus), Tracer (OpenTelemetry), structured Logger,
                HealthChecker, user feedback collection.""",
         """MetricsCollector（Prometheus）、Tracer（OpenTelemetry）、構造化 Logger、
                HealthChecker、フィードバック収集。"""),
        ("""EmbeddingClient with vector operations. TokenCounter (tiktoken integration) and cost
                estimation for usage tracking.""",
         """EmbeddingClient のベクトル演算。TokenCounter（tiktoken 連携）と利用コスト見積もり。"""),
        ("""Plugin base class, PluginRegistry, HookManager, middleware chain. JSON mode config,
                SchemaGenerator, OutputValidator.""",
         """Plugin 基底クラス、PluginRegistry、HookManager、ミドルウェア。JSON モード設定、
                SchemaGenerator、OutputValidator。"""),
    ],
    "es": [
        ("""Same layered architecture as the Rust runtime —protocol-driven, operator-based,
              resilient by default.""",
         """Misma arquitectura por capas que el runtime Rust: orientada a protocolo, por operadores
              y con resiliencia opt-in."""),
        ("""ProtocolLoader (local/env/GitHub), Pydantic manifest models, JSON Schema validator,
                hot-reload support.""",
         """ProtocolLoader (local/env/GitHub), modelos Pydantic de manifiesto, validador JSON Schema
                y hot-reload."""),
        ("""Decoder (SSE, JSON Lines, Anthropic SSE), Selector (JSONPath), Accumulator, FanOut,
                EventMapper (protocol-driven, default, Anthropic).""",
         """Decoder (SSE, JSON Lines, Anthropic SSE), Selector (JSONPath), Accumulator, FanOut,
                EventMapper (protocolo / default / Anthropic)."""),
        ("""ModelManager, ModelArray, selection strategies (round-robin, weighted, cost-based,
                quality-based). Pre-configured catalogs for major providers.""",
         """ModelManager, ModelArray y estrategias (round-robin, ponderada, coste, calidad).
                Catálogos preconfigurados para proveedores principales."""),
        ("""MetricsCollector (Prometheus), Tracer (OpenTelemetry), structured Logger,
                HealthChecker, user feedback collection.""",
         """MetricsCollector (Prometheus), Tracer (OpenTelemetry), Logger estructurado,
                HealthChecker y recogida de feedback."""),
        ("""EmbeddingClient with vector operations. TokenCounter (tiktoken integration) and cost
                estimation for usage tracking.""",
         """EmbeddingClient con operaciones vectoriales. TokenCounter (tiktoken) y estimación de coste."""),
        ("""Plugin base class, PluginRegistry, HookManager, middleware chain. JSON mode config,
                SchemaGenerator, OutputValidator.""",
         """Clase base Plugin, PluginRegistry, HookManager y middleware. Config JSON mode,
                SchemaGenerator, OutputValidator."""),
    ],
}


def main() -> None:
    for locale, pairs in PY.items():
        path = PAGES / locale / "python" / "index.astro"
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"patched {path.relative_to(PAGES.parent.parent)}")


if __name__ == "__main__":
    main()
