---
title: Ecosystem Architecture
description: How AI-Protocol, ai-lib-rust, and ai-lib-python work together as an integrated ecosystem.
---

# Ecosystem Architecture

The AI-Lib ecosystem is built on a clean three-layer architecture where each layer has a distinct responsibility.

## The Three Layers

### 1. Protocol Layer — AI-Protocol

The **specification** layer. YAML manifests define:

- **Provider manifests** (`providers/*.yaml`) — Endpoint, auth, parameter mappings, streaming decoder, error classification for each of 30+ providers
- **Model registry** (`models/*.yaml`) — Model instances with context windows, capabilities, pricing
- **Core specification** (`spec.yaml`) — Standard parameters, events, error types, retry policies
- **Schemas** (`schemas/`) — JSON Schema validation for all configuration

The protocol layer is **language-agnostic**. It's consumed by any runtime in any language.

### 2. Runtime Layer — Rust & Python SDKs

The **execution** layer. Runtimes implement:

- **Protocol loading** — Read and validate manifests from local files, env vars, or GitHub
- **Request compilation** — Convert unified requests to provider-specific HTTP calls
- **Streaming pipeline** — Decode, select, accumulate, and map provider responses to unified events
- **Resilience** — Circuit breaker, rate limiting, retry, fallback
- **Extensions** — Embeddings, caching, batching, plugins

Both runtimes share the same architecture:

| Concept | Rust | Python |
|---------|------|--------|
| Client | `AiClient` | `AiClient` |
| Builder | `AiClientBuilder` | `AiClientBuilder` |
| Request | `ChatRequestBuilder` | `ChatRequestBuilder` |
| Events | `StreamingEvent` enum | `StreamingEvent` class |
| Transport | reqwest (tokio) | httpx (asyncio) |
| Types | Rust structs | Pydantic v2 models |

### 3. Application Layer — Your Code

Applications use the unified runtime API. A single `AiClient` interface works across all providers:

```
Your App → AiClient → Protocol Manifest → Provider API
```

Switch providers by changing one model identifier. No code changes.

## Data Flow

Here's what happens when you call `client.chat().user("Hello").stream()`:

1. **AiClient** receives the request
2. **ProtocolLoader** provides the provider manifest
3. **Request compiler** maps standard params to provider-specific JSON
4. **Transport** sends the HTTP request with correct auth/headers
5. **Pipeline** processes the streaming response:
   - **Decoder** converts bytes → JSON frames (SSE or NDJSON)
   - **Selector** filters relevant frames using JSONPath
   - **Accumulator** assembles partial tool calls
   - **EventMapper** converts frames → unified `StreamingEvent`
6. **Application** iterates over unified events

## Protocol Loading

Both runtimes search for protocol manifests in this order:

1. **Custom path** — Explicitly set in builder
2. **Environment variable** — `AI_PROTOCOL_DIR` or `AI_PROTOCOL_PATH`
3. **Relative paths** — `ai-protocol/` or `../ai-protocol/` from working directory
4. **GitHub fallback** — Downloads from `hiddenpath/ai-protocol` repository

This means you can start developing without any local setup — the runtimes will fetch manifests from GitHub automatically.

## Relationship to MCP

AI-Protocol and MCP (Model Context Protocol) are **complementary**:

- **MCP** handles high-level concerns — tool registration, context management, agent coordination
- **AI-Protocol** handles low-level concerns — API normalization, streaming format conversion, error classification

They operate at different layers and can be used together.

## Next Steps

- **[AI-Protocol Overview](/protocol/overview/)** — Deep dive into the specification
- **[Rust SDK](/rust/overview/)** — Explore the Rust runtime
- **[Python SDK](/python/overview/)** — Explore the Python runtime
