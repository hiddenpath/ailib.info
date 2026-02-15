---
title: Rust SDK Overview
description: Architecture and design of ai-lib-rust — the high-performance Rust runtime for AI-Protocol.
---

# Rust SDK Overview

**ai-lib-rust** (v0.7.1) is the high-performance Rust runtime for the AI-Protocol specification. It implements a protocol-driven architecture where all provider behavior comes from configuration, not code.

## V2 Protocol Alignment

ai-lib-rust v0.7.1 aligns with the AI-Protocol V2 specification:

- **Standard Error Codes**: 13-variant `StandardErrorCode` enum (E1001–E9999) integrated into all error paths
- **Feature Flags**: 7 capability features (`embeddings`, `batch`, `guardrails`, `tokens`, `telemetry`, `routing_mvp`, `interceptors`) plus the `full` meta-feature
- **Compliance Testing**: 20/20 cross-runtime test cases passing
- **Structured Output**: JSON mode with schema validation

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
| `embeddings` | EmbeddingClient, vector operations |
| `batch` | BatchCollector, BatchExecutor |
| `guardrails` | Content filtering, PII detection |
| `tokens` | Token counting, cost estimation |
| `telemetry` | Advanced observability sinks |
| `routing_mvp` | CustomModelManager, ModelArray, load balancing strategies |
| `interceptors` | InterceptorPipeline for logging, metrics, audit |

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
