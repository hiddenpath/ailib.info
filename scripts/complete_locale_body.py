#!/usr/bin/env python3
"""Complete body translations for zh-cn / ja / es runtime landing pages."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "src" / "pages"

# Shared strings appearing on rust / python / go (and often ts) pages
COMMON_ZH = [
    (">Key Features</h2>", ">核心特性</h2>"),
    (">Internal Architecture</h2>", ">内部架构</h2>"),
    (">Module Overview</h2>", ">模块概览</h2>"),
    (">Simple, Unified API</h2>", ">统一、简洁的 API</h2>"),
    (">Documentation</h2>", ">文档</h2>"),
    (">Quick Start</a", ">快速开始</a"),
    (">Full Documentation</a", ">完整文档</a"),
    (">Start Building with Rust</h2>", ">开始使用 Rust 构建</h2>"),
    (">Start Building with Python</h2>", ">开始使用 Python 构建</h2>"),
    (">Start Building with Go</h2>", ">开始使用 Go 构建</h2>"),
    ("<span class=\"text-[var(--text)]\">for AI-Protocol.</span>",
     "<span class=\"text-[var(--text)]\">适用于 AI-Protocol。</span>"),
    # Shared feature / prose blocks (rust-like pages)
    ("V2 Error Codes & Feature Flags", "V2 错误码与 Feature 开关"),
    ("""13 V2 standard error codes for consistent error handling across providers.
                Feature-gated modules: 7 optional features plus a full meta-feature for minimal or
                complete builds.""",
     """13 个 V2 标准错误码，跨服务商统一错误处理。
                Feature 门控模块：7 个可选能力，外加 full 元特性，可按需精简或完整构建。"""),
    ("Operator-Based Pipeline", "算子流式管道"),
    ("""Streaming responses flow through composable operators: Decoder &rarr; Selector
                &rarr; Accumulator &rarr; FanOut &rarr; EventMapper. Each stage is
                protocol-configured.""",
     """流式响应经可组合算子处理：Decoder &rarr; Selector
                &rarr; Accumulator &rarr; FanOut &rarr; EventMapper。各阶段均由协议配置驱动。"""),
    ("Protocol + Pipeline", "协议 + 管道"),
    ("""<code>AiClient</code> loads manifests and runs the operator pipeline
                (Decoder &rarr; Selector &rarr; Accumulator &rarr; EventMapper). V1 and V2 manifest paths supported.""",
     """<code>AiClient</code> 加载清单并运行算子管道
                （Decoder &rarr; Selector &rarr; Accumulator &rarr; EventMapper）。支持 V1 / V2 清单路径。"""),
    ("E/P Workspace", "E/P 工作区"),
    ("""<code>ai-lib-core</code> (execution) and <code>ai-lib-contact</code> (policy) ship as
                separate crates; <code>ai-lib-rust</code> re-exports a stable facade.""",
     """<code>ai-lib-core</code>（执行层）与 <code>ai-lib-contact</code>（策略层）分 crate 发布；
                <code>ai-lib-rust</code> 再导出稳定门面。"""),
    ("""Built-in <code>max_inflight</code> backpressure on <code>AiClient</code>. Retry,
                rate limit, and circuit breaker live in <code>ai_lib_rust::resilience</code>""",
     """内置 <code>max_inflight</code> 背压。重试、限流与熔断位于 <code>ai_lib_rust::resilience</code>"""),
    ("Embeddings & Vectors", "嵌入与向量"),
    ("""EmbeddingClient with vector operations""",
     """EmbeddingClient 提供向量运算"""),
    ("Build semantic search and RAG applications natively.",
     "可原生构建语义检索与 RAG 应用。"),
    ("Cache & Batch", "缓存与批处理"),
    ("""Response caching with TTL (memory backend). Batch execution with configurable
                concurrency, timeout, and multiple processing strategies.""",
     """带 TTL 的响应缓存（内存后端）。批处理支持可配置并发、超时与多种执行策略。"""),
    ("Plugin System", "插件系统"),
    ("""Extensible plugin architecture with hooks and middleware chain. Add custom behavior
                without modifying core code. Guardrails for content filtering and PII detection.""",
     """可扩展插件架构，含钩子与中间件链。无需改动核心即可注入自定义行为。
                Guardrails 支持内容过滤与 PII 检测。"""),
    ("""The same code works across all 37 providers. Just change the model identifier""",
     """同一套代码适用于全部 37+ 服务商。只需更换模型标识符"""),
    ("""the
                protocol manifest handles everything else: endpoint, auth, parameter mapping,
                streaming format.""",
     """协议清单会处理其余一切：端点、鉴权、参数映射与流式格式。"""),
    ("""The builder pattern provides a fluent API for request construction. Stream results
                arrive as unified <code>StreamingEvent</code> types regardless of the underlying provider.""",
     """Builder 模式提供流畅的请求构造 API。流式结果统一为 <code>StreamingEvent</code>，
                与底层服务商无关。"""),
    ("""Five layers from user-facing API to HTTP transport. The streaming pipeline is the
              heart of the system.""",
     """从面向用户的 API 到 HTTP 传输共五层。流式管道是系统核心。"""),
    ("""AiClient, AiClientBuilder, ChatRequestBuilder, execution logic, policy engine,
                preflight checks, error classification, CallStats, CancelHandle.""",
     """AiClient、AiClientBuilder、ChatRequestBuilder、执行逻辑、策略引擎、
                预检、错误分类、CallStats、CancelHandle。"""),
    ("""ProtocolLoader (local/URL/GitHub), JSON Schema validator, ProtocolManifest
                structure, UnifiedRequest compilation, config types.""",
     """ProtocolLoader（本地 / URL / GitHub）、JSON Schema 校验、ProtocolManifest
                结构、UnifiedRequest 编译与配置类型。"""),
    ("""Decoder (SSE, JSON Lines), Selector (JSONPath), Accumulator (tool calls), FanOut
                (multi-candidate), EventMapper (unified events), Retry and Fallback operators.""",
     """Decoder（SSE、JSON Lines）、Selector（JSONPath）、Accumulator（工具调用）、FanOut
                （多候选）、EventMapper（统一事件），以及 Retry / Fallback 算子。"""),
    ("""HttpTransport (reqwest), API key resolution (keyring + env vars), proxy/timeout
                configuration, middleware support.""",
     """HttpTransport（reqwest）、API Key 解析（keyring + 环境变量）、代理 / 超时配置与中间件。"""),
    ("""Circuit breaker (open/half-open/closed), token bucket rate limiter, max-inflight
                semaphore backpressure.""",
     """熔断器（open / half-open / closed）、令牌桶限流、max-inflight 信号量背压。"""),
    ("""EmbeddingClient, EmbeddingClientBuilder, vector operations (cosine similarity,
                Euclidean distance, dot product).""",
     """EmbeddingClient、EmbeddingClientBuilder，以及向量运算（余弦相似度、欧氏距离、点积）。"""),
    ("""CacheManager with TTL (MemoryCache, NullCache). BatchCollector and BatchExecutor
                with concurrency control and multiple strategies.""",
     """带 TTL 的 CacheManager（MemoryCache、NullCache）。BatchCollector / BatchExecutor
                支持并发控制与多种策略。"""),
    ("""Plugin trait, PluginRegistry, HookManager, middleware chain. Guardrails with
                keyword/pattern filters and PII detection.""",
     """Plugin trait、PluginRegistry、HookManager 与中间件链。Guardrails 提供关键词 / 模式过滤与 PII 检测。"""),
]

COMMON_JA = [
    (">Key Features</h2>", ">主な機能</h2>"),
    (">Internal Architecture</h2>", ">内部アーキテクチャ</h2>"),
    (">Module Overview</h2>", ">モジュール概要</h2>"),
    (">Simple, Unified API</h2>", ">シンプルで統一された API</h2>"),
    (">Documentation</h2>", ">ドキュメント</h2>"),
    (">Quick Start</a", ">クイックスタート</a"),
    (">Full Documentation</a", ">完全なドキュメント</a"),
    (">Start Building with Rust</h2>", ">Rust で構築を始める</h2>"),
    (">Start Building with Python</h2>", ">Python で構築を始める</h2>"),
    (">Start Building with Go</h2>", ">Go で構築を始める</h2>"),
    ("<span class=\"text-[var(--text)]\">for AI-Protocol.</span>",
     "<span class=\"text-[var(--text)]\">AI-Protocol 向け。</span>"),
    ("V2 Error Codes & Feature Flags", "V2 エラーコードと Feature フラグ"),
    ("""13 V2 standard error codes for consistent error handling across providers.
                Feature-gated modules: 7 optional features plus a full meta-feature for minimal or
                complete builds.""",
     """プロバイダー横断で一貫したエラー処理を行う V2 標準エラーコード 13 種。
                Feature ゲート付きモジュール：任意 7 機能 + full メタ機能で最小／完全ビルドに対応。"""),
    ("Operator-Based Pipeline", "オペレーターベースのパイプライン"),
    ("""Streaming responses flow through composable operators: Decoder &rarr; Selector
                &rarr; Accumulator &rarr; FanOut &rarr; EventMapper. Each stage is
                protocol-configured.""",
     """ストリーミング応答は合成可能なオペレーターを通過します：Decoder &rarr; Selector
                &rarr; Accumulator &rarr; FanOut &rarr; EventMapper。各段はプロトコル設定で駆動。"""),
    ("Protocol + Pipeline", "プロトコル + パイプライン"),
    ("""<code>AiClient</code> loads manifests and runs the operator pipeline
                (Decoder &rarr; Selector &rarr; Accumulator &rarr; EventMapper). V1 and V2 manifest paths supported.""",
     """<code>AiClient</code> がマニフェストを読み込み、オペレーターパイプラインを実行
                （Decoder &rarr; Selector &rarr; Accumulator &rarr; EventMapper）。V1 / V2 パス対応。"""),
    ("E/P Workspace", "E/P ワークスペース"),
    ("""<code>ai-lib-core</code> (execution) and <code>ai-lib-contact</code> (policy) ship as
                separate crates; <code>ai-lib-rust</code> re-exports a stable facade.""",
     """<code>ai-lib-core</code>（実行）と <code>ai-lib-contact</code>（ポリシー）は別クレート。
                <code>ai-lib-rust</code> が安定したファサードを再エクスポートします。"""),
    ("""Built-in <code>max_inflight</code> backpressure on <code>AiClient</code>. Retry,
                rate limit, and circuit breaker live in <code>ai_lib_rust::resilience</code>""",
     """<code>AiClient</code> に組み込みの <code>max_inflight</code> 背圧。再試行・レート制限・サーキットブレーカーは
                <code>ai_lib_rust::resilience</code>"""),
    ("Embeddings & Vectors", "埋め込みとベクトル"),
    ("Build semantic search and RAG applications natively.",
     "セマンティック検索や RAG をネイティブに構築できます。"),
    ("Cache & Batch", "キャッシュとバッチ"),
    ("""Response caching with TTL (memory backend). Batch execution with configurable
                concurrency, timeout, and multiple processing strategies.""",
     """TTL 付きレスポンスキャッシュ（メモリ）。並行度・タイムアウト・複数戦略を設定可能なバッチ実行。"""),
    ("Plugin System", "プラグインシステム"),
    ("""Extensible plugin architecture with hooks and middleware chain. Add custom behavior
                without modifying core code. Guardrails for content filtering and PII detection.""",
     """フックとミドルウェアチェーンを備えた拡張可能なプラグイン。コアを変更せずに振る舞いを追加。
                Guardrails によるコンテンツフィルタと PII 検出。"""),
    ("""The same code works across all 37 providers. Just change the model identifier""",
     """同じコードが 37+ プロバイダーで動作します。モデル識別子を変えるだけ"""),
    ("""the
                protocol manifest handles everything else: endpoint, auth, parameter mapping,
                streaming format.""",
     """プロトコルマニフェストがエンドポイント、認証、パラメータ対応、ストリーミング形式を処理します。"""),
    ("""The builder pattern provides a fluent API for request construction. Stream results
                arrive as unified <code>StreamingEvent</code> types regardless of the underlying provider.""",
     """ビルダーパターンで流暢なリクエスト構築。ストリーム結果は基盤プロバイダーに依らず
                統一された <code>StreamingEvent</code> として届きます。"""),
    ("""Five layers from user-facing API to HTTP transport. The streaming pipeline is the
              heart of the system.""",
     """ユーザー向け API から HTTP トランスポートまでの 5 層。ストリーミングパイプラインが中核です。"""),
    ("""AiClient, AiClientBuilder, ChatRequestBuilder, execution logic, policy engine,
                preflight checks, error classification, CallStats, CancelHandle.""",
     """AiClient、AiClientBuilder、ChatRequestBuilder、実行ロジック、ポリシーエンジン、
                事前チェック、エラー分類、CallStats、CancelHandle。"""),
    ("""ProtocolLoader (local/URL/GitHub), JSON Schema validator, ProtocolManifest
                structure, UnifiedRequest compilation, config types.""",
     """ProtocolLoader（ローカル / URL / GitHub）、JSON Schema 検証、ProtocolManifest、
                UnifiedRequest コンパイル、設定型。"""),
    ("""Decoder (SSE, JSON Lines), Selector (JSONPath), Accumulator (tool calls), FanOut
                (multi-candidate), EventMapper (unified events), Retry and Fallback operators.""",
     """Decoder（SSE、JSON Lines）、Selector（JSONPath）、Accumulator（ツール呼び出し）、FanOut、
                EventMapper、Retry / Fallback オペレーター。"""),
    ("""HttpTransport (reqwest), API key resolution (keyring + env vars), proxy/timeout
                configuration, middleware support.""",
     """HttpTransport（reqwest）、API キー解決（keyring + 環境変数）、プロキシ / タイムアウト、ミドルウェア。"""),
    ("""Circuit breaker (open/half-open/closed), token bucket rate limiter, max-inflight
                semaphore backpressure.""",
     """サーキットブレーカー（open / half-open / closed）、トークンバケット制限、max-inflight 背圧。"""),
    ("""EmbeddingClient, EmbeddingClientBuilder, vector operations (cosine similarity,
                Euclidean distance, dot product).""",
     """EmbeddingClient、EmbeddingClientBuilder、ベクトル演算（コサイン類似度、ユークリッド距離、内積）。"""),
    ("""CacheManager with TTL (MemoryCache, NullCache). BatchCollector and BatchExecutor
                with concurrency control and multiple strategies.""",
     """TTL 付き CacheManager（MemoryCache、NullCache）。並行制御と複数戦略の BatchCollector / BatchExecutor。"""),
    ("""Plugin trait, PluginRegistry, HookManager, middleware chain. Guardrails with
                keyword/pattern filters and PII detection.""",
     """Plugin trait、PluginRegistry、HookManager、ミドルウェア。キーワード / パターンフィルタと PII 検出の Guardrails。"""),
]

COMMON_ES = [
    (">Key Features</h2>", ">Características clave</h2>"),
    (">Internal Architecture</h2>", ">Arquitectura interna</h2>"),
    (">Module Overview</h2>", ">Resumen de módulos</h2>"),
    (">Simple, Unified API</h2>", ">API simple y unificada</h2>"),
    (">Documentation</h2>", ">Documentación</h2>"),
    (">Quick Start</a", ">Inicio rápido</a"),
    (">Full Documentation</a", ">Documentación completa</a"),
    (">Start Building with Rust</h2>", ">Empieza a construir con Rust</h2>"),
    (">Start Building with Python</h2>", ">Empieza a construir con Python</h2>"),
    (">Start Building with Go</h2>", ">Empieza a construir con Go</h2>"),
    ("<span class=\"gradient-text-rust\">Rust Runtime</span>",
     "<span class=\"gradient-text-rust\">Runtime Rust</span>"),
    ("<span class=\"gradient-text-python\">Python Runtime</span>",
     "<span class=\"gradient-text-python\">Runtime Python</span>"),
    ("<span class=\"gradient-text-rust\">Go Runtime</span>",
     "<span class=\"gradient-text-rust\">Runtime Go</span>"),
    ("<span class=\"gradient-text\">TypeScript Runtime</span>",
     "<span class=\"gradient-text\">Runtime TypeScript</span>"),
    ("<span class=\"text-[var(--text)]\">for AI-Protocol.</span>",
     "<span class=\"text-[var(--text)]\">para AI-Protocol.</span>"),
    ("V2 Error Codes & Feature Flags", "Códigos de error V2 y feature flags"),
    ("""13 V2 standard error codes for consistent error handling across providers.
                Feature-gated modules: 7 optional features plus a full meta-feature for minimal or
                complete builds.""",
     """13 códigos de error estándar V2 para un manejo coherente entre proveedores.
                Módulos por feature: 7 opcionales más un meta-feature full para builds mínimos o completos."""),
    ("Operator-Based Pipeline", "Pipeline basado en operadores"),
    ("""Streaming responses flow through composable operators: Decoder &rarr; Selector
                &rarr; Accumulator &rarr; FanOut &rarr; EventMapper. Each stage is
                protocol-configured.""",
     """Las respuestas en streaming pasan por operadores componibles: Decoder &rarr; Selector
                &rarr; Accumulator &rarr; FanOut &rarr; EventMapper. Cada etapa se configura por protocolo."""),
    ("Protocol + Pipeline", "Protocolo + Pipeline"),
    ("""<code>AiClient</code> loads manifests and runs the operator pipeline
                (Decoder &rarr; Selector &rarr; Accumulator &rarr; EventMapper). V1 and V2 manifest paths supported.""",
     """<code>AiClient</code> carga manifiestos y ejecuta el pipeline de operadores
                (Decoder &rarr; Selector &rarr; Accumulator &rarr; EventMapper). Compatibilidad con rutas V1 y V2."""),
    ("E/P Workspace", "Workspace E/P"),
    ("""<code>ai-lib-core</code> (execution) and <code>ai-lib-contact</code> (policy) ship as
                separate crates; <code>ai-lib-rust</code> re-exports a stable facade.""",
     """<code>ai-lib-core</code> (ejecución) y <code>ai-lib-contact</code> (política) se publican
                como crates separados; <code>ai-lib-rust</code> reexporta una fachada estable."""),
    ("""Built-in <code>max_inflight</code> backpressure on <code>AiClient</code>. Retry,
                rate limit, and circuit breaker live in <code>ai_lib_rust::resilience</code>""",
     """Backpressure <code>max_inflight</code> integrado en <code>AiClient</code>. Reintentos,
                límite de tasa y circuit breaker viven en <code>ai_lib_rust::resilience</code>"""),
    ("Embeddings & Vectors", "Embeddings y vectores"),
    ("Build semantic search and RAG applications natively.",
     "Construye búsqueda semántica y RAG de forma nativa."),
    ("Cache & Batch", "Caché y lotes"),
    ("""Response caching with TTL (memory backend). Batch execution with configurable
                concurrency, timeout, and multiple processing strategies.""",
     """Caché de respuestas con TTL (memoria). Ejecución por lotes con concurrencia,
                timeout y varias estrategias configurables."""),
    ("Plugin System", "Sistema de plugins"),
    ("""Extensible plugin architecture with hooks and middleware chain. Add custom behavior
                without modifying core code. Guardrails for content filtering and PII detection.""",
     """Arquitectura de plugins extensible con hooks y cadena de middleware. Añade comportamiento
                sin modificar el núcleo. Guardrails para filtrado de contenido y detección de PII."""),
    ("""The same code works across all 37 providers. Just change the model identifier""",
     """El mismo código funciona con los 37+ proveedores. Solo cambia el identificador del modelo"""),
    ("""the
                protocol manifest handles everything else: endpoint, auth, parameter mapping,
                streaming format.""",
     """el manifiesto del protocolo gestiona el resto: endpoint, autenticación, mapeo de parámetros
                y formato de streaming."""),
    ("""The builder pattern provides a fluent API for request construction. Stream results
                arrive as unified <code>StreamingEvent</code> types regardless of the underlying provider.""",
     """El patrón builder ofrece una API fluida para construir peticiones. Los resultados en stream
                llegan como <code>StreamingEvent</code> unificados, independientemente del proveedor."""),
    ("""Five layers from user-facing API to HTTP transport. The streaming pipeline is the
              heart of the system.""",
     """Cinco capas desde la API de usuario hasta el transporte HTTP. El pipeline de streaming
              es el corazón del sistema."""),
    ("""AiClient, AiClientBuilder, ChatRequestBuilder, execution logic, policy engine,
                preflight checks, error classification, CallStats, CancelHandle.""",
     """AiClient, AiClientBuilder, ChatRequestBuilder, lógica de ejecución, motor de políticas,
                comprobaciones previas, clasificación de errores, CallStats, CancelHandle."""),
    ("""ProtocolLoader (local/URL/GitHub), JSON Schema validator, ProtocolManifest
                structure, UnifiedRequest compilation, config types.""",
     """ProtocolLoader (local/URL/GitHub), validador JSON Schema, estructura ProtocolManifest,
                compilación de UnifiedRequest y tipos de configuración."""),
    ("""Decoder (SSE, JSON Lines), Selector (JSONPath), Accumulator (tool calls), FanOut
                (multi-candidate), EventMapper (unified events), Retry and Fallback operators.""",
     """Decoder (SSE, JSON Lines), Selector (JSONPath), Accumulator (llamadas a herramientas), FanOut,
                EventMapper y operadores Retry / Fallback."""),
    ("""HttpTransport (reqwest), API key resolution (keyring + env vars), proxy/timeout
                configuration, middleware support.""",
     """HttpTransport (reqwest), resolución de API key (keyring + variables de entorno),
                proxy/timeout y middleware."""),
    ("""Circuit breaker (open/half-open/closed), token bucket rate limiter, max-inflight
                semaphore backpressure.""",
     """Circuit breaker (open/half-open/closed), limitador token bucket y backpressure max-inflight."""),
    ("""EmbeddingClient, EmbeddingClientBuilder, vector operations (cosine similarity,
                Euclidean distance, dot product).""",
     """EmbeddingClient, EmbeddingClientBuilder y operaciones vectoriales (similitud coseno,
                distancia euclídea, producto punto)."""),
    ("""CacheManager with TTL (MemoryCache, NullCache). BatchCollector and BatchExecutor
                with concurrency control and multiple strategies.""",
     """CacheManager con TTL (MemoryCache, NullCache). BatchCollector y BatchExecutor
                con control de concurrencia y varias estrategias."""),
    ("""Plugin trait, PluginRegistry, HookManager, middleware chain. Guardrails with
                keyword/pattern filters and PII detection.""",
     """Plugin trait, PluginRegistry, HookManager y cadena de middleware. Guardrails con
                filtros por palabra/patrón y detección de PII."""),
]

# Python-specific
PY_ZH = [
    ("V2 Error Codes & Capability Extras", "V2 错误码与能力 Extras"),
    ("""13 V2 standard error codes for consistent error handling. Capability-based extras: 8
                optional extras plus a full extra for minimal or complete installs.""",
     """13 个 V2 标准错误码，统一错误处理。基于能力的 extras：8 个可选包，外加 full 完整安装。"""),
    ("Async-First Design", "异步优先设计"),
    ("""Native async/await throughout. httpx-powered transport with connection pooling.
                CancellableStream for graceful stream termination.""",
     """全程原生 async/await。基于 httpx 的传输与连接池。
                CancellableStream 支持优雅终止流。"""),
    ("Pydantic v2 Types", "Pydantic v2 类型"),
    ("""Full type hints with Pydantic v2 validation. ProtocolManifest, Message,
                ContentBlock, StreamingEvent —all type-safe with runtime validation.""",
     """完整类型注解与 Pydantic v2 校验。ProtocolManifest、Message、
                ContentBlock、StreamingEvent 均类型安全并带运行时验证。"""),
    ("Resilient Executor", "韧性执行器"),
    ("""ResilientExecutor combines backpressure, rate limiting, circuit breaker, and retry
                with exponential backoff. PreflightChecker gates requests before execution.""",
     """ResilientExecutor 组合背压、限流、熔断与指数退避重试。
                PreflightChecker 在执行前门控请求。"""),
    ("Model Routing", "模型路由"),
    ("""ModelManager with ModelArray for intelligent model selection. Strategies include
                round-robin, weighted, cost-based, and quality-based routing.""",
     """ModelManager + ModelArray 实现智能选型。策略含轮询、加权、成本优先与质量优先。"""),
    ("Production Telemetry", "生产级遥测"),
    ("""MetricsCollector with Prometheus export. Distributed tracing via OpenTelemetry.
                Structured logging. Health monitoring. User feedback collection.""",
     """MetricsCollector 支持 Prometheus 导出。OpenTelemetry 分布式追踪。
                结构化日志、健康监控与用户反馈采集。"""),
    ("Structured Output", "结构化输出"),
    ("""JSON mode configuration, schema generation from Pydantic models, output validation.
                Guardrails with content filters and PII detection.""",
     """JSON 模式配置、由 Pydantic 模型生成 schema、输出校验。
                Guardrails 提供内容过滤与 PII 检测。"""),
    (">Pythonic & Intuitive</h2>", ">符合 Python 习惯、直观易用</h2>"),
    ("""A clean, Pythonic API that feels natural. Create a client from a model identifier,
                build requests with a fluent builder, and iterate over unified streaming events.""",
     """干净、符合 Python 习惯的 API。用模型标识创建客户端，
                以流畅 Builder 构造请求，并迭代统一的流式事件。"""),
    ("""The same code works across all providers. Switch from OpenAI to Anthropic to""",
     """同一套代码适用于所有服务商。从 OpenAI 切换到 Anthropic 再到"""),
]

PY_JA = [
    ("V2 Error Codes & Capability Extras", "V2 エラーコードと Capability Extras"),
    ("""13 V2 standard error codes for consistent error handling. Capability-based extras: 8
                optional extras plus a full extra for minimal or complete installs.""",
     """一貫したエラー処理のための V2 標準エラーコード 13 種。能力ベース extras：任意 8 + full。"""),
    ("Async-First Design", "非同期ファースト設計"),
    ("""Native async/await throughout. httpx-powered transport with connection pooling.
                CancellableStream for graceful stream termination.""",
     """全体でネイティブ async/await。httpx トランスポートと接続プール。
                CancellableStream で優雅なストリーム終了。"""),
    ("Pydantic v2 Types", "Pydantic v2 型"),
    ("Resilient Executor", "レジリエント実行器"),
    ("""ResilientExecutor combines backpressure, rate limiting, circuit breaker, and retry
                with exponential backoff. PreflightChecker gates requests before execution.""",
     """ResilientExecutor は背圧・レート制限・サーキットブレーカー・指数バックオフ再試行を統合。
                PreflightChecker が実行前にリクエストをゲート。"""),
    ("Model Routing", "モデルルーティング"),
    ("Production Telemetry", "本番テレメトリ"),
    ("Structured Output", "構造化出力"),
    (">Pythonic & Intuitive</h2>", ">Pythonic で直感的</h2>"),
    ("""A clean, Pythonic API that feels natural. Create a client from a model identifier,
                build requests with a fluent builder, and iterate over unified streaming events.""",
     """自然に感じるクリーンな Pythonic API。モデル ID からクライアントを作成し、
                流暢なビルダーでリクエストを組み立て、統一ストリームイベントを反復します。"""),
]

PY_ES = [
    ("V2 Error Codes & Capability Extras", "Códigos de error V2 y extras de capacidad"),
    ("""13 V2 standard error codes for consistent error handling. Capability-based extras: 8
                optional extras plus a full extra for minimal or complete installs.""",
     """13 códigos de error estándar V2. Extras por capacidad: 8 opcionales más un extra full."""),
    ("Async-First Design", "Diseño async-first"),
    ("""Native async/await throughout. httpx-powered transport with connection pooling.
                CancellableStream for graceful stream termination.""",
     """async/await nativo de extremo a extremo. Transporte httpx con pool de conexiones.
                CancellableStream para terminar streams con gracia."""),
    ("Pydantic v2 Types", "Tipos Pydantic v2"),
    ("Resilient Executor", "Ejecutor resiliente"),
    ("""ResilientExecutor combines backpressure, rate limiting, circuit breaker, and retry
                with exponential backoff. PreflightChecker gates requests before execution.""",
     """ResilientExecutor combina backpressure, límite de tasa, circuit breaker y reintentos
                con backoff exponencial. PreflightChecker filtra peticiones antes de ejecutar."""),
    ("Model Routing", "Enrutamiento de modelos"),
    ("Production Telemetry", "Telemetría de producción"),
    ("Structured Output", "Salida estructurada"),
    (">Pythonic & Intuitive</h2>", ">Pythonic e intuitivo</h2>"),
    ("""A clean, Pythonic API that feels natural. Create a client from a model identifier,
                build requests with a fluent builder, and iterate over unified streaming events.""",
     """Una API limpia y pythonic. Crea un cliente desde un identificador de modelo,
                construye peticiones con un builder fluido e itera eventos de streaming unificados."""),
]

# TypeScript-specific
TS_ZH = [
    ("V2 Manifest Parsing", "V2 清单解析"),
    ("""Parse and load V2 protocol manifests with standard error codes (13 codes).
                Provider-agnostic configuration with zero hardcoded logic.""",
     """解析并加载带 13 个标准错误码的 V2 协议清单。
                与服务商无关的配置，零硬编码逻辑。"""),
    ("Resilience Patterns", "韧性模式"),
    ("""Built-in RetryPolicy, CircuitBreaker, RateLimiter, and Backpressure.
                PreflightChecker for unified request gating.""",
     """内置 RetryPolicy、CircuitBreaker、RateLimiter 与 Backpressure。
                PreflightChecker 提供统一请求门控。"""),
    ("Model Routing", "模型路由"),
    ("""ModelManager with CostBasedSelector, QualityBasedSelector, and FallbackChain. Smart
                model selection for cost and quality optimization.""",
     """ModelManager 配合 CostBasedSelector、QualityBasedSelector 与 FallbackChain。
                按成本与质量智能选型。"""),
    ("Multimodal Support", "多模态支持"),
    ("""SttClient for speech-to-text, TtsClient for text-to-speech, RerankerClient for
                document reranking. Full multimodal content block support.""",
     """SttClient（语音转文字）、TtsClient（文字转语音）、RerankerClient（文档重排）。
                完整多模态内容块支持。"""),
    ("MCP Tool Bridge", "MCP 工具桥接"),
    ("""Bridge MCP tools to AI-Protocol format. Seamlessly integrate MCP servers with
                unified tool calling interface.""",
     """将 MCP 工具桥接到 AI-Protocol 格式。以统一工具调用接口无缝集成 MCP 服务器。"""),
    ("Batch & Plugins", "批处理与插件"),
    ("""BatchExecutor for parallel processing with configurable concurrency. Plugin system
                with hooks for request/response interception.""",
     """BatchExecutor 支持可配置并发的并行处理。插件系统通过钩子拦截请求 / 响应。"""),
    ("Create client with model ID", "使用模型 ID 创建客户端"),
    ("Build chat request with fluent API", "用流畅 API 构建聊天请求"),
    ("Execute or stream the response", "执行或流式获取响应"),
    ("""The same code works across all 37 providers. Just change the model identifier —the
                protocol manifest handles everything else.""",
     """同一套代码适用于全部 37+ 服务商。只需更换模型标识符——其余由协议清单处理。"""),
    ("""Protocol-driven architecture with type-safe execution, resilient by default, and fully
              extensible.""",
     """协议驱动架构：类型安全执行、默认可选韧性、完全可扩展。"""),
    ("""AiClient, ChatRequestBuilder, ChatResponse, CallStats, CancelToken,
                CancellableStream, Unified error codes.""",
     """AiClient、ChatRequestBuilder、ChatResponse、CallStats、CancelToken、
                CancellableStream，以及统一错误码。"""),
    ("""ProtocolLoader (local/fetch/GitHub), V2 manifest definitions, JSON Schema Validator,
                Provider-agnostic models.""",
     """ProtocolLoader（本地 / fetch / GitHub）、V2 清单定义、JSON Schema 校验器、
                与服务商无关的模型类型。"""),
    ("""Decoder (SSE, JSON Lines), Selector (JSONPath), Accumulator, FanOut, EventMapper
                (protocol-driven).""",
     """Decoder（SSE、JSON Lines）、Selector（JSONPath）、Accumulator、FanOut、EventMapper
                （协议驱动）。"""),
    ("""RetryPolicy, CircuitBreaker, RateLimiter, Backpressure, PreflightChecker,
                SignalsSnapshot, FallbackChain.""",
     """RetryPolicy、CircuitBreaker、RateLimiter、Backpressure、PreflightChecker、
                SignalsSnapshot、FallbackChain。"""),
    ("""ModelManager, QualityBasedSelector, CostBasedSelector, FallbackChain for intelligent
                model selection.""",
     """ModelManager、QualityBasedSelector、CostBasedSelector、FallbackChain，用于智能选型。"""),
    ("""McpBridge, McpTool definitions to seamlessly integrate Model Context Protocol
                servers.""",
     """McpBridge 与 McpTool 定义，用于无缝集成 Model Context Protocol 服务器。"""),
    ("""SttClient, TtsClient, RerankerClient, fully supporting multimodal inputs and
                specialized models.""",
     """SttClient、TtsClient、RerankerClient，完整支持多模态输入与专用模型。"""),
    ("""PluginRegistry, Hooks. BatchExecutor for concurrent batch execution with concurrency
                limits.""",
     """PluginRegistry、Hooks。BatchExecutor 支持带并发上限的批量执行。"""),
    ("Quick Start →", "快速开始 →"),
    ("AiClient API →", "AiClient API →"),
    ("Streaming →", "流式处理 →"),
    ("Resilience →", "韧性模式 →"),
    ("Advanced →", "高级特性 →"),
    ("Overview →", "概述 →"),
    ("Get up and running in minutes.", "几分钟内即可上手。"),
    ("Complete API reference.", "完整 API 参考。"),
    ("Real-time response handling.", "实时响应处理。"),
    ("Production-ready patterns.", "生产级韧性模式。"),
    ("Embeddings, MCP, plugins.", "嵌入、MCP、插件。"),
    ("Architecture and concepts.", "架构与核心概念。"),
]

TS_JA = [
    ("V2 Manifest Parsing", "V2 マニフェスト解析"),
    ("""Parse and load V2 protocol manifests with standard error codes (13 codes).
                Provider-agnostic configuration with zero hardcoded logic.""",
     """標準エラーコード（13 種）付き V2 プロトコルマニフェストを解析・読み込み。
                ハードコードなしのプロバイダー非依存設定。"""),
    ("Resilience Patterns", "レジリエンスパターン"),
    ("""Built-in RetryPolicy, CircuitBreaker, RateLimiter, and Backpressure.
                PreflightChecker for unified request gating.""",
     """組み込みの RetryPolicy、CircuitBreaker、RateLimiter、Backpressure。
                PreflightChecker による統一リクエストゲート。"""),
    ("Model Routing", "モデルルーティング"),
    ("""ModelManager with CostBasedSelector, QualityBasedSelector, and FallbackChain. Smart
                model selection for cost and quality optimization.""",
     """ModelManager と CostBasedSelector / QualityBasedSelector / FallbackChain。
                コストと品質を最適化するスマート選択。"""),
    ("Multimodal Support", "マルチモーダル対応"),
    ("""SttClient for speech-to-text, TtsClient for text-to-speech, RerankerClient for
                document reranking. Full multimodal content block support.""",
     """音声認識の SttClient、音声合成の TtsClient、再ランキングの RerankerClient。
                マルチモーダルコンテンツブロックを完全サポート。"""),
    ("MCP Tool Bridge", "MCP ツールブリッジ"),
    ("""Bridge MCP tools to AI-Protocol format. Seamlessly integrate MCP servers with
                unified tool calling interface.""",
     """MCP ツールを AI-Protocol 形式へ橋渡し。統一ツール呼び出しで MCP サーバーを統合。"""),
    ("Batch & Plugins", "バッチとプラグイン"),
    ("""BatchExecutor for parallel processing with configurable concurrency. Plugin system
                with hooks for request/response interception.""",
     """並行度設定可能な BatchExecutor。リクエスト / レスポンス傍受用フック付きプラグイン。"""),
    ("Create client with model ID", "モデル ID でクライアントを作成"),
    ("Build chat request with fluent API", "流暢な API でチャットリクエストを構築"),
    ("Execute or stream the response", "実行またはストリームで応答を取得"),
    ("""The same code works across all 37 providers. Just change the model identifier —the
                protocol manifest handles everything else.""",
     """同じコードが 37+ プロバイダーで動作。モデル識別子を変えるだけで、残りはマニフェストが処理。"""),
    ("""Protocol-driven architecture with type-safe execution, resilient by default, and fully
              extensible.""",
     """プロトコル駆動アーキテクチャ：型安全な実行、既定のレジリエンス、完全な拡張性。"""),
    ("Quick Start →", "クイックスタート →"),
    ("Streaming →", "ストリーミング →"),
    ("Resilience →", "レジリエンス →"),
    ("Advanced →", "高度な機能 →"),
    ("Overview →", "概要 →"),
    ("Get up and running in minutes.", "数分で始められます。"),
    ("Complete API reference.", "完全な API リファレンス。"),
    ("Real-time response handling.", "リアルタイム応答処理。"),
    ("Production-ready patterns.", "本番向けパターン。"),
    ("Embeddings, MCP, plugins.", "埋め込み、MCP、プラグイン。"),
    ("Architecture and concepts.", "アーキテクチャと概念。"),
    ("""AiClient, ChatRequestBuilder, ChatResponse, CallStats, CancelToken,
                CancellableStream, Unified error codes.""",
     """AiClient、ChatRequestBuilder、ChatResponse、CallStats、CancelToken、
                CancellableStream、統一エラーコード。"""),
    ("""ProtocolLoader (local/fetch/GitHub), V2 manifest definitions, JSON Schema Validator,
                Provider-agnostic models.""",
     """ProtocolLoader（ローカル / fetch / GitHub）、V2 マニフェスト、JSON Schema 検証、
                プロバイダー非依存モデル。"""),
    ("""Decoder (SSE, JSON Lines), Selector (JSONPath), Accumulator, FanOut, EventMapper
                (protocol-driven).""",
     """Decoder（SSE、JSON Lines）、Selector（JSONPath）、Accumulator、FanOut、EventMapper
                （プロトコル駆動）。"""),
    ("""RetryPolicy, CircuitBreaker, RateLimiter, Backpressure, PreflightChecker,
                SignalsSnapshot, FallbackChain.""",
     """RetryPolicy、CircuitBreaker、RateLimiter、Backpressure、PreflightChecker、
                SignalsSnapshot、FallbackChain。"""),
    ("""ModelManager, QualityBasedSelector, CostBasedSelector, FallbackChain for intelligent
                model selection.""",
     """ModelManager、QualityBasedSelector、CostBasedSelector、FallbackChain による知的選択。"""),
    ("""McpBridge, McpTool definitions to seamlessly integrate Model Context Protocol
                servers.""",
     """McpBridge と McpTool 定義で Model Context Protocol サーバーを統合。"""),
    ("""SttClient, TtsClient, RerankerClient, fully supporting multimodal inputs and
                specialized models.""",
     """SttClient、TtsClient、RerankerClient。マルチモーダル入力と専用モデルを完全サポート。"""),
    ("""PluginRegistry, Hooks. BatchExecutor for concurrent batch execution with concurrency
                limits.""",
     """PluginRegistry、Hooks。並行上限付き BatchExecutor。"""),
]

TS_ES = [
    ("V2 Manifest Parsing", "Análisis de manifiestos V2"),
    ("""Parse and load V2 protocol manifests with standard error codes (13 codes).
                Provider-agnostic configuration with zero hardcoded logic.""",
     """Analiza y carga manifiestos V2 con 13 códigos de error estándar.
                Configuración agnóstica al proveedor, sin lógica hardcodeada."""),
    ("Resilience Patterns", "Patrones de resiliencia"),
    ("""Built-in RetryPolicy, CircuitBreaker, RateLimiter, and Backpressure.
                PreflightChecker for unified request gating.""",
     """RetryPolicy, CircuitBreaker, RateLimiter y Backpressure integrados.
                PreflightChecker para el filtrado unificado de peticiones."""),
    ("Model Routing", "Enrutamiento de modelos"),
    ("""ModelManager with CostBasedSelector, QualityBasedSelector, and FallbackChain. Smart
                model selection for cost and quality optimization.""",
     """ModelManager con CostBasedSelector, QualityBasedSelector y FallbackChain.
                Selección inteligente por coste y calidad."""),
    ("Multimodal Support", "Soporte multimodal"),
    ("""SttClient for speech-to-text, TtsClient for text-to-speech, RerankerClient for
                document reranking. Full multimodal content block support.""",
     """SttClient (voz a texto), TtsClient (texto a voz), RerankerClient (reordenación).
                Soporte completo de bloques de contenido multimodal."""),
    ("MCP Tool Bridge", "Puente de herramientas MCP"),
    ("""Bridge MCP tools to AI-Protocol format. Seamlessly integrate MCP servers with
                unified tool calling interface.""",
     """Conecta herramientas MCP al formato AI-Protocol. Integra servidores MCP
                con una interfaz unificada de tool calling."""),
    ("Batch & Plugins", "Lotes y plugins"),
    ("""BatchExecutor for parallel processing with configurable concurrency. Plugin system
                with hooks for request/response interception.""",
     """BatchExecutor para procesamiento paralelo con concurrencia configurable.
                Sistema de plugins con hooks de petición/respuesta."""),
    ("Create client with model ID", "Crear cliente con ID de modelo"),
    ("Build chat request with fluent API", "Construir chat con API fluida"),
    ("Execute or stream the response", "Ejecutar o transmitir la respuesta"),
    ("""The same code works across all 37 providers. Just change the model identifier —the
                protocol manifest handles everything else.""",
     """El mismo código funciona con los 37+ proveedores. Solo cambia el identificador —
                el manifiesto gestiona el resto."""),
    ("""Protocol-driven architecture with type-safe execution, resilient by default, and fully
              extensible.""",
     """Arquitectura orientada a protocolo: ejecución tipada, resiliencia opcional y
              extensibilidad total."""),
    ("Quick Start →", "Inicio rápido →"),
    ("Streaming →", "Streaming →"),
    ("Resilience →", "Resiliencia →"),
    ("Advanced →", "Avanzado →"),
    ("Overview →", "Resumen →"),
    ("Get up and running in minutes.", "Ponte en marcha en minutos."),
    ("Complete API reference.", "Referencia completa de la API."),
    ("Real-time response handling.", "Manejo de respuestas en tiempo real."),
    ("Production-ready patterns.", "Patrones listos para producción."),
    ("Embeddings, MCP, plugins.", "Embeddings, MCP, plugins."),
    ("Architecture and concepts.", "Arquitectura y conceptos."),
    ("""AiClient, ChatRequestBuilder, ChatResponse, CallStats, CancelToken,
                CancellableStream, Unified error codes.""",
     """AiClient, ChatRequestBuilder, ChatResponse, CallStats, CancelToken,
                CancellableStream y códigos de error unificados."""),
    ("""ProtocolLoader (local/fetch/GitHub), V2 manifest definitions, JSON Schema Validator,
                Provider-agnostic models.""",
     """ProtocolLoader (local/fetch/GitHub), definiciones de manifiesto V2, validador JSON Schema
                y modelos agnósticos al proveedor."""),
    ("""Decoder (SSE, JSON Lines), Selector (JSONPath), Accumulator, FanOut, EventMapper
                (protocol-driven).""",
     """Decoder (SSE, JSON Lines), Selector (JSONPath), Accumulator, FanOut, EventMapper
                (orientado a protocolo)."""),
    ("""RetryPolicy, CircuitBreaker, RateLimiter, Backpressure, PreflightChecker,
                SignalsSnapshot, FallbackChain.""",
     """RetryPolicy, CircuitBreaker, RateLimiter, Backpressure, PreflightChecker,
                SignalsSnapshot, FallbackChain."""),
    ("""ModelManager, QualityBasedSelector, CostBasedSelector, FallbackChain for intelligent
                model selection.""",
     """ModelManager, QualityBasedSelector, CostBasedSelector y FallbackChain para selección inteligente."""),
    ("""McpBridge, McpTool definitions to seamlessly integrate Model Context Protocol
                servers.""",
     """McpBridge y definiciones McpTool para integrar servidores Model Context Protocol."""),
    ("""SttClient, TtsClient, RerankerClient, fully supporting multimodal inputs and
                specialized models.""",
     """SttClient, TtsClient, RerankerClient con soporte multimodal y modelos especializados."""),
    ("""PluginRegistry, Hooks. BatchExecutor for concurrent batch execution with concurrency
                limits.""",
     """PluginRegistry, Hooks. BatchExecutor para ejecución concurrente con límites."""),
]

HERO_META = {
    "zh-cn": {
        "rust": [
            ("ai-lib-rust | High-Performance Rust Runtime for AI-Protocol",
             "ai-lib-rust | AI-Protocol 高性能 Rust 运行时"),
            ("content=\"ai-lib-rust is the high-performance Rust runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
             "content=\"ai-lib-rust 是 AI-Protocol 的高性能 Rust 运行时。清单驱动的 Pipeline + AiClient，E/P 工作区，feature 门控能力模块。\""),
            ("<span class=\"gradient-text-rust\">Rust Runtime</span>",
             "<span class=\"gradient-text-rust\">Rust 运行时</span>"),
            ("""High-performance Rust runtime for AI-Protocol. Manifest-driven
              <code>Pipeline</code> + <code>AiClient</code>, E/P workspace
              (<code>ai-lib-core</code> + <code>ai-lib-contact</code>), 13 V2 error codes,
              and feature-gated capability modules.""",
             """AI-Protocol 高性能 Rust 运行时（v1.0.1）。默认路径：清单 → Pipeline → HttpTransport。
              E/P 工作区（<code>ai-lib-core</code> + <code>ai-lib-contact</code>），13 个 V2 标准错误码，
              以及 feature 门控的能力模块。"""),
        ],
        "python": [
            ("ai-lib-python | Python Runtime for AI-Protocol",
             "ai-lib-python | AI-Protocol Python 运行时"),
            ("<span class=\"gradient-text-python\">Python Runtime</span>",
             "<span class=\"gradient-text-python\">Python 运行时</span>"),
            ("""Async, protocol-driven AI client (v1.0.0). Default path: manifest → Pipeline →
              httpx transport. Pydantic v2 types, 13 V2 error codes, pip extras for capabilities,
              and opt-in resilience via AiClientBuilder. Python 3.10+.""",
             """异步、协议驱动的 AI 客户端（v1.0.0）。默认路径：清单 → Pipeline → httpx。
              Pydantic v2 类型、13 个 V2 错误码、pip extras，以及通过 AiClientBuilder 可选启用的韧性。Python 3.10+。"""),
        ],
        "go": [
            ("ai-lib-go | High-Performance Go Runtime for AI-Protocol",
             "ai-lib-go | AI-Protocol Go 运行时"),
            ("<span class=\"gradient-text-rust\">Go Runtime</span>",
             "<span class=\"gradient-text-rust\">Go 运行时</span>"),
            ("""Go protocol runtime (v1.0.0). pkg/ailib manifest HTTP chat; pkg/contact fallback policy.
              13 V2 error codes, ChatStream SSE decoder, ExecutionMetadata on responses. Go 1.21+.""",
             """Go 协议运行时（v1.0.0）。pkg/ailib 负责清单 HTTP 聊天；pkg/contact 提供回退策略。
              13 个 V2 错误码、ChatStream SSE 解码器，响应附带 ExecutionMetadata。Go 1.21+。"""),
            ("""High-performance, protocol-driven AI client. V2 standard error codes (13 codes),
              feature flags (7 features + full meta-feature), zero hardcoded provider logic,
              operator-based streaming pipeline, compile-time type safety, and sub-millisecond
              overhead.""",
             """Go 协议运行时（v1.0.0）。pkg/ailib 负责清单 HTTP 聊天；pkg/contact 提供回退策略。
              13 个 V2 错误码、ChatStream SSE 解码器。Go 1.21+。"""),
        ],
        "ts": [
            ("ai-lib-ts | TypeScript/Node.js Runtime for AI-Protocol",
             "ai-lib-ts | AI-Protocol TypeScript/Node.js 运行时"),
            ("<span class=\"gradient-text\">TypeScript Runtime</span>",
             "<span class=\"gradient-text\">TypeScript 运行时</span>"),
            ("""Protocol-driven, streaming-first TypeScript/Node.js runtime. V2 manifest parsing,
              standard error codes, Resilience patterns, Model routing, MCP bridge, and multimodal
              support.""",
             """协议驱动的 TypeScript/Node.js 运行时（v1.0.0）。默认聊天路径为 HttpTransport + 清单解析。
              提供 /core 与 /contact 入口，13 个 V2 错误码。"""),
        ],
    },
    "ja": {
        "rust": [
            ("ai-lib-rust | High-Performance Rust Runtime for AI-Protocol",
             "ai-lib-rust | AI-Protocol 高性能 Rust ランタイム"),
            ("content=\"ai-lib-rust is the high-performance Rust runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
             "content=\"AI-Protocol 向け高性能 Rust ランタイム。マニフェスト駆動 Pipeline + AiClient、E/P ワークスペース。\""),
            ("<span class=\"gradient-text-rust\">Rust Runtime</span>",
             "<span class=\"gradient-text-rust\">Rust ランタイム</span>"),
            ("""High-performance Rust runtime for AI-Protocol. Manifest-driven
              <code>Pipeline</code> + <code>AiClient</code>, E/P workspace
              (<code>ai-lib-core</code> + <code>ai-lib-contact</code>), 13 V2 error codes,
              and feature-gated capability modules.""",
             """AI-Protocol 向け高性能 Rust ランタイム（v1.0.1）。マニフェスト → Pipeline → HttpTransport。
              E/P ワークスペース（ai-lib-core + ai-lib-contact）、V2 エラーコード 13 種、feature ゲート能力。"""),
        ],
        "python": [
            ("ai-lib-python | Python Runtime for AI-Protocol",
             "ai-lib-python | AI-Protocol Python ランタイム"),
            ("<span class=\"gradient-text-python\">Python Runtime</span>",
             "<span class=\"gradient-text-python\">Python ランタイム</span>"),
            ("""Async, protocol-driven AI client (v1.0.0). Default path: manifest → Pipeline →
              httpx transport. Pydantic v2 types, 13 V2 error codes, pip extras for capabilities,
              and opt-in resilience via AiClientBuilder. Python 3.10+.""",
             """非同期のプロトコル駆動 AI クライアント（v1.0.0）。既定経路：マニフェスト → Pipeline → httpx。
              Pydantic v2、V2 エラーコード 13 種、pip extras、オプトイン resilience。Python 3.10+。"""),
        ],
        "go": [
            ("ai-lib-go | High-Performance Go Runtime for AI-Protocol",
             "ai-lib-go | AI-Protocol Go ランタイム"),
            ("<span class=\"gradient-text-rust\">Go Runtime</span>",
             "<span class=\"gradient-text-rust\">Go ランタイム</span>"),
            ("""Go protocol runtime (v1.0.0). pkg/ailib manifest HTTP chat; pkg/contact fallback policy.
              13 V2 error codes, ChatStream SSE decoder, ExecutionMetadata on responses. Go 1.21+.""",
             """Go プロトコルランタイム（v1.0.0）。pkg/ailib のマニフェスト HTTP チャットと pkg/contact フォールバック。
              V2 エラーコード 13 種、ChatStream SSE、ExecutionMetadata。Go 1.21+。"""),
            ("""High-performance, protocol-driven AI client. V2 standard error codes (13 codes),
              feature flags (7 features + full meta-feature), zero hardcoded provider logic,
              operator-based streaming pipeline, compile-time type safety, and sub-millisecond
              overhead.""",
             """Go プロトコルランタイム（v1.0.0）。pkg/ailib + pkg/contact。プロトコル優先 HTTP と ExecutionMetadata。Go 1.21+。"""),
        ],
        "ts": [
            ("ai-lib-ts | TypeScript/Node.js Runtime for AI-Protocol",
             "ai-lib-ts | AI-Protocol TypeScript/Node.js ランタイム"),
            ("<span class=\"gradient-text\">TypeScript Runtime</span>",
             "<span class=\"gradient-text\">TypeScript ランタイム</span>"),
            ("""Protocol-driven, streaming-first TypeScript/Node.js runtime. V2 manifest parsing,
              standard error codes, Resilience patterns, Model routing, MCP bridge, and multimodal
              support.""",
             """プロトコル駆動の TypeScript/Node.js ランタイム（v1.0.0）。HttpTransport + マニフェスト解析。
              /core と /contact、V2 エラーコード 13 種。"""),
        ],
    },
    "es": {
        "rust": [
            ("ai-lib-rust | High-Performance Rust Runtime for AI-Protocol",
             "ai-lib-rust | Runtime Rust de alto rendimiento para AI-Protocol"),
            ("content=\"ai-lib-rust is the high-performance Rust runtime for AI-Protocol. Operator-based streaming pipeline, compile-time safety, sub-millisecond overhead.\"",
             "content=\"Runtime Rust de alto rendimiento para AI-Protocol. Pipeline + AiClient basados en manifiestos, workspace E/P.\""),
            ("""High-performance Rust runtime for AI-Protocol. Manifest-driven
              <code>Pipeline</code> + <code>AiClient</code>, E/P workspace
              (<code>ai-lib-core</code> + <code>ai-lib-contact</code>), 13 V2 error codes,
              and feature-gated capability modules.""",
             """Runtime Rust de alto rendimiento para AI-Protocol (v1.0.1). Ruta: manifiesto → Pipeline → HttpTransport.
              Workspace E/P (ai-lib-core + ai-lib-contact), 13 códigos de error V2 y módulos por feature."""),
        ],
        "python": [
            ("ai-lib-python | Python Runtime for AI-Protocol",
             "ai-lib-python | Runtime Python para AI-Protocol"),
            ("""Async, protocol-driven AI client (v1.0.0). Default path: manifest → Pipeline →
              httpx transport. Pydantic v2 types, 13 V2 error codes, pip extras for capabilities,
              and opt-in resilience via AiClientBuilder. Python 3.10+.""",
             """Cliente AI asíncrono orientado a protocolo (v1.0.0). Ruta: manifiesto → Pipeline → httpx.
              Tipos Pydantic v2, 13 códigos V2, extras pip y resiliencia opt-in. Python 3.10+."""),
        ],
        "go": [
            ("ai-lib-go | High-Performance Go Runtime for AI-Protocol",
             "ai-lib-go | Runtime Go para AI-Protocol"),
            ("""Go protocol runtime (v1.0.0). pkg/ailib manifest HTTP chat; pkg/contact fallback policy.
              13 V2 error codes, ChatStream SSE decoder, ExecutionMetadata on responses. Go 1.21+.""",
             """Runtime Go orientado a protocolo (v1.0.0). pkg/ailib + pkg/contact, HTTP por manifiestos
              y ExecutionMetadata. Go 1.21+."""),
            ("""High-performance, protocol-driven AI client. V2 standard error codes (13 codes),
              feature flags (7 features + full meta-feature), zero hardcoded provider logic,
              operator-based streaming pipeline, compile-time type safety, and sub-millisecond
              overhead.""",
             """Runtime Go orientado a protocolo (v1.0.0). pkg/ailib + pkg/contact, HTTP por manifiestos
              y ExecutionMetadata. Go 1.21+."""),
        ],
        "ts": [
            ("ai-lib-ts | TypeScript/Node.js Runtime for AI-Protocol",
             "ai-lib-ts | Runtime TypeScript/Node.js para AI-Protocol"),
            ("""Protocol-driven, streaming-first TypeScript/Node.js runtime. V2 manifest parsing,
              standard error codes, Resilience patterns, Model routing, MCP bridge, and multimodal
              support.""",
             """Runtime TypeScript/Node.js orientado a protocolo (v1.0.0). HttpTransport + parsers de manifiesto.
              Entradas /core y /contact, 13 códigos de error V2."""),
        ],
    },
}


def apply(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def localize(en: str, locale: str, lang: str, runtime: str) -> str:
    out = en
    out = out.replace("const locale = 'en'", f"const locale = '{locale}'")
    out = out.replace('<html lang="en"', f'<html lang="{lang}"')
    for segment in ("styles/", "components/"):
        out = out.replace(f"'../../{segment}", f"'../../../{segment}")
    for segment in ("rust", "ts", "python", "go", "protocol", "quickstart", "ecosystem", "intro"):
        out = out.replace(f'href="/{segment}/', f'href="/{locale}/{segment}/')

    common = {"zh-cn": COMMON_ZH, "ja": COMMON_JA, "es": COMMON_ES}[locale]
    out = apply(out, common)
    out = apply(out, HERO_META[locale].get(runtime, []))

    if runtime == "python":
        out = apply(out, {"zh-cn": PY_ZH, "ja": PY_JA, "es": PY_ES}[locale])
    if runtime == "ts":
        out = apply(out, {"zh-cn": TS_ZH, "ja": TS_JA, "es": TS_ES}[locale])
    return out


def main() -> None:
    locales = [("zh-cn", "zh-CN"), ("ja", "ja"), ("es", "es")]
    for runtime in ("rust", "python", "go", "ts"):
        en = (PAGES / runtime / "index.astro").read_text(encoding="utf-8")
        for locale, lang in locales:
            out = localize(en, locale, lang, runtime)
            dest = PAGES / locale / runtime / "index.astro"
            dest.write_text(out, encoding="utf-8", newline="\n")
            print(f"wrote {dest.relative_to(ROOT)}")
    print("done")


if __name__ == "__main__":
    main()
