---
title: Introduction
description: Overview of the AI-Lib ecosystem — AI-Protocol specification and its Rust, Python, TypeScript, and Go runtime implementations.
---

# Welcome to AI-Lib

**AI-Lib** is an open-source ecosystem that standardizes how applications interact with AI models. Instead of writing provider-specific code for each AI service, you use a single unified API — and protocol configuration handles the rest.

## The Core Idea

> **All logic is operators, all configuration is protocol.**

Traditional AI SDKs embed provider-specific logic in code: different HTTP endpoints, different parameter names, different streaming formats, different error codes. When you switch providers, you rewrite code.

AI-Lib takes a different approach:

- **AI-Protocol** defines how to talk to each provider in YAML manifests
- **Runtime implementations** (Rust, Python, TypeScript, Go) read these manifests and execute requests
- **Zero hardcoded logic** — no `if provider == "openai"` branches anywhere

## Six Projects, One Ecosystem

- **ai-protocol** (v0.8.3): The provider-agnostic specification. Core schemas, V2 manifests, and validation tools.
- **ai-lib-rust** (v0.9.3): High-performance Rust runtime, published on crates.io.
- **ai-lib-python** (v0.8.3): Developer-friendly Python runtime, published on PyPI.
- **ai-lib-ts** (v0.5.3): TypeScript/Node.js runtime, published on npm.
- **ai-lib-go** (v0.0.1): High-concurrency Go runtime mapping to the V2 spec.
- **ai-protocol-mock** (v0.1.11): Unified mock server for integration testing across all runtimes.

The latest release cycle delivers full **V2 protocol** execution with governance gates: **MCP**, **Computer Use**, **Extended Multimodal**, and script-based release gates (`drift`, `manifest-consumption`, `compliance-matrix`, `fullchain`, `release-gate`) with `--report-only` staged rollout.

### AI-Protocol (Specification)

Since the v0.8.x milestone, **AI-Protocol V2** relies heavily on declarative configuration (`v2/providers/*.yaml`). Instead of burying provider-specific quirks in code, the ecosystem supports 37+ total providers (10 V2 + 27 V1) mapping directly via schema.

### ai-lib-rust (Rust Runtime)

High-performance runtime. Operator-based streaming pipeline processes responses through composable stages (Decoder → Selector → Accumulator → EventMapper). Built-in resilience with circuit breaker, rate limiter, and backpressure. Published on Crates.io.

### ai-lib-python (Python Runtime)

Developer-friendly runtime. Full async/await support, Pydantic v2 type safety, production-grade telemetry (OpenTelemetry + Prometheus), and intelligent model routing. Published on PyPI.

### ai-lib-ts (TypeScript Runtime)

Node.js runtime for the npm ecosystem. Manifest-driven V2 parsing, standardized errors, streaming, resilience modules, and compliance matrix execution aligned with Rust/Python.

### ai-lib-go (Go Runtime)

High-concurrency runtime optimized for server-side deployments. Direct V2 specification mapping, context-aware resilience, and efficient streaming interfaces.

## Key Features

- **37 providers** — OpenAI, Anthropic, Gemini, DeepSeek, Qwen, Moonshot, Zhipu, and many more (10 V2 + 27 V1)
- **Unified streaming** — Same `StreamingEvent` types regardless of provider
- **Protocol-driven** — All behavior defined in YAML, not code
- **MCP integration** — Built-in MCP tool bridge: convert MCP server tools to AI-Protocol format automatically
- **Computer Use** — Normalized GUI automation abstraction with safety policy enforcement
- **Extended multimodal** — Vision, audio, video input; audio and image output; omni-mode support
- **ProviderDriver** — Three concrete drivers (OpenAI, Anthropic, Gemini) with automatic API style detection
- **Capability Registry** — Dynamic module loading based on manifest capability declarations
- **CLI tool** — `ai-protocol-cli` for manifest validation, provider info, and compatibility checking
- **Hot-reload** — Update provider configs without restarting
- **Resilience** — Circuit breaker, rate limiting, retry, fallback
- **Tool calling** — Unified function calling across providers
- **Embeddings** — Vector operations and similarity search
- **Type safety** — Compile-time (Rust/Go) and runtime (Pydantic/TS) validation

## Runtime Comparison

| Capability       | Protocol Standard | Rust SDK                      | Python SDK            | TypeScript SDK              | Go SDK                       |
| ---------------- | ----------------- | ----------------------------- | --------------------- | --------------------------- | ---------------------------- |
| **Type System**  | JSON Schema       | Compile-time validation       | Runtime (Pydantic v2) | Compile-time (TypeScript)   | Compile-time (Go Structs)    |
| **Streaming**    | SSE / NDJSON      | tokio async streams           | async generators      | AsyncIterator + fetch       | Iterators (iter.Seq2)        |
| **Resilience**   | Retry policy spec | Circuit breaker, backpressure | ResilientExecutor     | RetryPolicy, CircuitBreaker | Context timeouts, auto-retry |
| **MCP**          | mcp.json spec     | McpToolBridge                 | McpToolBridge         | McpToolBridge               | To be implemented            |
| **Distribution** | GitHub / npm      | Crates.io                     | PyPI                  | npm                         | goproxy                      |

## Next Steps

- **[Quick Start](/quickstart/)** — Get up and running in minutes
- **[Ecosystem Architecture](/ecosystem/)** — Understand how the pieces fit together
- **[AI-Protocol](/protocol/overview/)** — Dive into the specification
- **[Rust SDK](/rust/overview/)** — Start with Rust
- **[Python SDK](/python/overview/)** — Start with Python
- **[TypeScript SDK](/ts/overview/)** — Start with TypeScript
- **[Go SDK](/go/overview/)** — Start with Go
