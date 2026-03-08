---
title: Introduction
description: Overview of the AI-Lib ecosystem — AI-Protocol specification and its Rust, Python, and TypeScript runtime implementations.
---

# Welcome to AI-Lib

**AI-Lib** is an open-source ecosystem that standardizes how applications interact with AI models. Instead of writing provider-specific code for each AI service, you use a single unified API — and protocol configuration handles the rest.

## The Core Idea

> **All logic is operators, all configuration is protocol.**

Traditional AI SDKs embed provider-specific logic in code: different HTTP endpoints, different parameter names, different streaming formats, different error codes. When you switch providers, you rewrite code.

AI-Lib takes a different approach:

- **AI-Protocol** defines how to talk to each provider in YAML manifests
- **Runtime implementations** (Rust, Python, TypeScript) read these manifests and execute requests
- **Zero hardcoded logic** — no `if provider == "openai"` branches anywhere

## Five Projects, One Ecosystem

| Project | Role | Language | Version | Distribution |
|---------|------|----------|---------|---------------|
| **[AI-Protocol](/protocol/)** | Specification layer | YAML/JSON | v0.8.2 | GitHub |
| **[ai-lib-rust](/rust/)** | Runtime implementation | Rust | v0.9.2 | [Crates.io](https://crates.io/crates/ai-lib) |
| **[ai-lib-python](/python/)** | Runtime implementation | Python | v0.8.2 | [PyPI](https://pypi.org/project/ai-lib-python/) |
| **[ai-lib-ts](/ts/)** | Runtime implementation | TypeScript | v0.5.2 | [npm](https://www.npmjs.com/package/@hiddenpath/ai-lib-ts) |
| **ai-protocol-mock** | Mock/testing layer | Python | v0.1.10 | GitHub |

The latest release cycle delivers full **V2 protocol** execution with governance gates: **MCP**, **Computer Use**, **Extended Multimodal**, and script-based release gates (`drift`, `manifest-consumption`, `compliance-matrix`, `fullchain`, `release-gate`) with `--report-only` staged rollout.

### AI-Protocol (Specification)

The foundation. YAML manifests describe 37 AI providers (6 V2 + 36 V1): their endpoints, authentication, parameter mappings, streaming decoder configurations, error classification rules, MCP/CU/multimodal capabilities, and more. JSON Schema validates everything.

### ai-lib-rust (Rust Runtime)

High-performance runtime. Operator-based streaming pipeline processes responses through composable stages (Decoder → Selector → Accumulator → EventMapper). Built-in resilience with circuit breaker, rate limiter, and backpressure. Published on Crates.io.

### ai-lib-python (Python Runtime)

Developer-friendly runtime. Full async/await support, Pydantic v2 type safety, production-grade telemetry (OpenTelemetry + Prometheus), and intelligent model routing. Published on PyPI.

### ai-lib-ts (TypeScript Runtime)

Node.js runtime for the npm ecosystem. Manifest-driven V2 parsing, standardized errors, streaming, resilience modules, and compliance matrix execution aligned with Rust/Python.

## Key Features

- **37 providers** — OpenAI, Anthropic, Gemini, DeepSeek, Qwen, Moonshot, Zhipu, and many more (6 V2 + 36 V1)
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
- **Type safety** — Compile-time (Rust) and runtime (Pydantic) validation

## Next Steps

- **[Quick Start](/quickstart/)** — Get up and running in minutes
- **[Ecosystem Architecture](/ecosystem/)** — Understand how the pieces fit together
- **[AI-Protocol](/protocol/overview/)** — Dive into the specification
- **[Rust SDK](/rust/overview/)** — Start with Rust
- **[Python SDK](/python/overview/)** — Start with Python
- **[TypeScript SDK](/ts/overview/)** — Start with TypeScript
