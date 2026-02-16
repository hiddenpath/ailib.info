---
title: Rust SDK Overview
description: Architecture and design of ai-lib-rust — the high-performance Rust runtime for AI-Protocol.
---

# Rust SDK Overview

**ai-lib-rust** (v0.8.0) is the high-performance Rust runtime for the AI-Protocol specification. It implements a protocol-driven architecture where all provider behavior comes from configuration, not code.

## V2 Protocol Alignment

ai-lib-rust v0.8.0 fully implements the V2 protocol specification:

- **V2 Manifest Loading**: Three-ring manifest parser (`ManifestV2`) with V1 auto-promotion
- **ProviderDriver**: `Box<dyn ProviderDriver>` abstraction with OpenAI, Anthropic, and Gemini drivers
- **Capability Registry**: Feature-gate based dynamic capability detection and module loading
- **MCP Tool Bridge**: `McpToolBridge` for converting MCP tools to AI-Protocol format with namespace isolation
- **Computer Use**: `ComputerAction` enum + `SafetyPolicy` for protocol-driven safety enforcement
- **Extended Multimodal**: `MultimodalCapabilities` for modality detection, format validation, and capability checking
- **Standard Error Codes**: 13-variant `StandardErrorCode` enum (E1001–E9999) integrated into all error paths
- **185+ Tests**: Comprehensive coverage including 6 V2 integration tests and 53 CLI validations

## Architecture

The SDK is organized into distinct layers:

### Client Layer (`client/`)
The user-facing API:
- **AiClient** — Main entry point, created from model identifiers
- **AiClientBuilder** — Configuration builder with resilience settings
- **ChatRequestBuilder** — Fluent API for building chat requests
- **CallStats** — Request/response statistics (tokens, latency)
- **CancelHandle** — Graceful stream cancellation

### Protocol Layer (`protocol/`)
Loads and interprets AI-Protocol manifests:
- **ProtocolLoader** — Loads from local files, env vars, or GitHub
- **ProtocolManifest** — Parsed provider configuration
- **Validator** — JSON Schema validation
- **UnifiedRequest** — Standard request format compiled to provider-specific JSON

### Pipeline Layer (`pipeline/`)
The heart of streaming processing — an operator-based pipeline:
- **Decoder** — Converts byte streams to JSON frames (SSE, JSON Lines)
- **Selector** — Filters frames using JSONPath expressions
- **Accumulator** — Statefully assembles tool calls from partial chunks
- **FanOut** — Expands multi-candidate responses
- **EventMapper** — Converts frames to unified `StreamingEvent` types
- **Retry/Fallback** — Pipeline-level retry and fallback operators

### Transport Layer (`transport/`)
HTTP communication:
- **HttpTransport** — reqwest-based HTTP client
- **Auth** — API key resolution (OS keyring → env vars)
- **Middleware** — Transport middleware for logging, metrics

### Resilience Layer (`resilience/`)
Production reliability patterns:
- **CircuitBreaker** — Open/half-open/closed failure isolation
- **RateLimiter** — Token bucket algorithm
- **Backpressure** — max_inflight semaphore

### V2 Modules (feature-gated)

- **drivers/** — `ProviderDriver` trait + OpenAI, Anthropic, Gemini implementations; auto-selected by manifest `api_style`
- **registry/** — `CapabilityRegistry` for runtime module loading based on manifest declarations
- **mcp/** — `McpToolBridge` for MCP tool format conversion, namespace isolation (`mcp__{server}__{tool}`), and provider-specific config extraction
- **computer_use/** — `ComputerAction` enum (screenshot, mouse, keyboard, browser, file ops) + `SafetyPolicy` (domain allowlist, sensitive path protection, max actions per turn)
- **multimodal/** — `MultimodalCapabilities` for modality detection, format validation (image, audio, video), and content block validation

### Additional Modules
- **embeddings/** — EmbeddingClient with vector operations
- **cache/** — Response caching with TTL (MemoryCache)
- **batch/** — BatchCollector and BatchExecutor
- **tokens/** — Token counting and cost estimation
- **plugins/** — Plugin trait, registry, hooks, middleware
- **guardrails/** — Content filtering, PII detection
- **routing/** — Model routing and load balancing (feature-gated)
- **telemetry/** — Feedback sink for user feedback collection

## Key Dependencies

| Crate | Purpose |
|-------|---------|
| `tokio` | Async runtime |
| `reqwest` | HTTP client |
| `serde` / `serde_json` / `serde_yaml` | Serialization |
| `jsonschema` | Manifest validation |
| `tracing` | Structured logging |
| `arc-swap` | Hot-reload support |
| `notify` | File watching |
| `keyring` | OS keyring integration |

## Feature Flags

Optional features enabled via Cargo (use `full` to enable all):

| Feature | What it enables |
|---------|----------------|
| `v2` | V2 manifest loading, ProviderDriver, Capability Registry |
| `mcp` | MCP tool bridge, namespace isolation, provider config extraction |
| `computer_use` | Computer Use actions, safety policy enforcement |
| `multimodal` | Extended multimodal capabilities, format validation |
| `embeddings` | EmbeddingClient, vector operations |
| `batch` | BatchCollector, BatchExecutor |
| `guardrails` | Content filtering, PII detection |
| `tokens` | Token counting, cost estimation |
| `telemetry` | Advanced observability sinks |
| `routing_mvp` | CustomModelManager, ModelArray, load balancing strategies |
| `interceptors` | InterceptorPipeline for logging, metrics, audit |
| `reasoning` | Extended thinking, reasoning traces |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `AI_PROTOCOL_DIR` | Protocol manifest directory |
| `<PROVIDER>_API_KEY` | Provider API key (e.g., `OPENAI_API_KEY`) |
| `AI_LIB_RPS` | Rate limit (requests per second) |
| `AI_LIB_BREAKER_FAILURE_THRESHOLD` | Circuit breaker threshold |
| `AI_LIB_MAX_INFLIGHT` | Max concurrent requests |
| `AI_HTTP_TIMEOUT_SECS` | HTTP timeout |

## Next Steps

- **[Quick Start](/rust/quickstart/)** — Get running in minutes
- **[AiClient API](/rust/client/)** — Client usage details
- **[Streaming Pipeline](/rust/streaming/)** — Pipeline deep dive
- **[Resilience](/rust/resilience/)** — Reliability patterns
