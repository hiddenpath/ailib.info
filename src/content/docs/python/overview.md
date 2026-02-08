---
title: Python SDK Overview
description: Architecture and design of ai-lib-python — the developer-friendly Python runtime for AI-Protocol.
---

# Python SDK Overview

**ai-lib-python** (v0.5.0) is the official Python runtime for AI-Protocol. It provides a developer-friendly, fully async interface with Pydantic v2 type safety and production-grade telemetry.

## Architecture

The Python SDK mirrors the Rust runtime's layered architecture:

### Client Layer (`client/`)
- **AiClient** — Main entry point with factory methods
- **AiClientBuilder** — Fluent configuration builder
- **ChatRequestBuilder** — Request construction
- **ChatResponse** / **CallStats** — Response types
- **CancelToken** / **CancellableStream** — Stream cancellation

### Protocol Layer (`protocol/`)
- **ProtocolLoader** — Loads manifests from local/env/GitHub with caching
- **ProtocolManifest** — Pydantic models for provider configurations
- **Validator** — JSON Schema validation (fastjsonschema)

### Pipeline Layer (`pipeline/`)
- **Decoder** — SSE, JSON Lines, Anthropic SSE decoders
- **Selector** — JSONPath-based frame selection (jsonpath-ng)
- **Accumulator** — Tool call assembly
- **FanOut** — Multi-candidate expansion
- **EventMapper** — Protocol-driven, Default, and Anthropic mappers

### Transport Layer (`transport/`)
- **HttpTransport** — httpx-based async HTTP with streaming
- **Auth** — API key resolution from env vars and keyring
- **ConnectionPool** — Connection pooling for performance

### Resilience Layer (`resilience/`)
- **ResilientExecutor** — Combines all patterns
- **RetryPolicy** — Exponential backoff
- **RateLimiter** — Token bucket
- **CircuitBreaker** — Failure isolation
- **Backpressure** — Concurrency limiting
- **FallbackChain** — Multi-target failover
- **PreflightChecker** — Unified request gating

### Routing Layer (`routing/`)
- **ModelManager** — Model registration and selection
- **ModelArray** — Load balancing across endpoints
- **Selection strategies** — Round-robin, weighted, cost-based, quality-based

### Telemetry Layer (`telemetry/`)
- **MetricsCollector** — Prometheus metrics export
- **Tracer** — OpenTelemetry distributed tracing
- **Logger** — Structured logging
- **HealthChecker** — Service health monitoring
- **FeedbackCollector** — User feedback

### Additional Modules
- **embeddings/** — EmbeddingClient with vector operations
- **cache/** — Multi-backend caching (memory, disk)
- **tokens/** — TokenCounter (tiktoken) and cost estimation
- **batch/** — BatchCollector/Executor with concurrency control
- **plugins/** — Plugin base, registry, hooks, middleware
- **structured/** — JSON mode, schema generation, output validation
- **guardrails/** — Content filtering, validators

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `httpx` | Async HTTP client |
| `pydantic` | Data validation and types |
| `pydantic-settings` | Settings management |
| `fastjsonschema` | Manifest validation |
| `jsonpath-ng` | JSONPath expressions |
| `pyyaml` | YAML parsing |

### Optional

| Extra | Packages |
|-------|----------|
| `[telemetry]` | OpenTelemetry, Prometheus |
| `[tokenizer]` | tiktoken |
| `[full]` | All of the above + watchdog, keyring |

## Python Version

Requires **Python 3.10+**.

## Next Steps

- **[Quick Start](/python/quickstart/)** — Get running fast
- **[AiClient API](/python/client/)** — Detailed API guide
- **[Streaming Pipeline](/python/streaming/)** — Pipeline internals
- **[Resilience](/python/resilience/)** — Reliability patterns
