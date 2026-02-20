---
title: Ecosystem Architecture
description: How AI-Protocol, ai-lib-rust, and ai-lib-python work together as an integrated ecosystem.
---

# Ecosystem Architecture

The AI-Lib ecosystem is built on a clean three-layer architecture where each layer has a distinct responsibility. Current versions: **AI-Protocol v0.7.6**, **ai-lib-rust v0.8.5**, **ai-lib-python v0.7.4**, **ai-protocol-mock v0.1.7**.

## The Three Layers

### 1. Protocol Layer — AI-Protocol

The **specification** layer. YAML manifests define:

- **Provider manifests** (`v1/providers/` + `v2/providers/`) — Endpoint, auth, parameter mappings, streaming decoder, error classification for 38 providers (8 V2 + 36 V1)
- **Model registry** (`models/*.yaml`) — Model instances with context windows, capabilities, pricing
- **Core specification** (`spec.yaml`, `v2-alpha/spec.yaml`) — Standard parameters, events, error types, retry policies
- **V2 Schemas** (`schemas/v2/`) — JSON Schema for provider, MCP, Computer Use, multimodal, context policy, and ProviderContract
- **V2 ProviderContract** — API style declaration, capability matrix, action mapping, degradation strategy

The protocol layer is **language-agnostic**. It's consumed by any runtime in any language.

### 2. Runtime Layer — Rust & Python SDKs

The **execution** layer. Runtimes implement:

- **Protocol loading** — Read and validate manifests from local files, env vars, or GitHub
- **Request compilation** — Convert unified requests to provider-specific HTTP calls
- **Streaming pipeline** — Decode, select, accumulate, and map provider responses to unified events
- **Resilience** — Circuit breaker, rate limiting, retry, fallback
- **Extensions** — Embeddings, caching, batching, plugins

Both runtimes share the same architecture with cross-runtime parity:

| Concept | Rust | Python |
|---------|------|--------|
| Client | `AiClient` | `AiClient` |
| Builder | `AiClientBuilder` | `AiClientBuilder` |
| Request | `ChatRequestBuilder` | `ChatRequestBuilder` |
| Events | `StreamingEvent` enum | `StreamingEvent` class |
| Transport | reqwest (tokio) | httpx (asyncio) |
| Types | Rust structs | Pydantic v2 models |
| **V2 Driver** | `Box<dyn ProviderDriver>` | `ProviderDriver` ABC |
| **Registry** | `CapabilityRegistry` (feature-gate) | `CapabilityRegistry` (pip extras) |
| **MCP Bridge** | `McpToolBridge` | `McpToolBridge` |
| **Computer Use** | `ComputerAction` + `SafetyPolicy` | `ComputerAction` + `SafetyPolicy` |
| **Multimodal** | `MultimodalCapabilities` | `MultimodalCapabilities` |

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

## V2 Protocol Architecture

The V2 protocol (v0.7.0) delivers a complete **three-layer pyramid** with three new capability modules:

### Three-Layer Pyramid

- **L1 Core Protocol** — Message format, standard error codes (E1001–E9999), version declaration
- **L2 Capability Extensions** — Streaming, vision, tools, MCP, Computer Use, multimodal — each controlled by feature flags
- **L3 Environment Profile** — API keys, endpoints, retry policies — environment-specific configuration

### Concentric Circle Manifest Model

V2 manifests are organized in three rings:

- **Ring 1 Core Skeleton** (required) — Minimal fields: endpoint, auth, parameter mappings, model list
- **Ring 2 Capability Mapping** (conditional) — Streaming config, tool mapping, MCP integration, Computer Use actions
- **Ring 3 Advanced Extensions** (optional) — Custom headers, rate limit headers, context management policies

### ProviderDriver Abstraction

Both runtimes implement a **ProviderDriver** abstraction that normalizes three distinct API styles:

| API Style | Provider | Request Format | Streaming Format |
|-----------|----------|----------------|------------------|
| `OpenAiCompatible` | OpenAI, DeepSeek, Moonshot | `messages` array | SSE `data: {...}` |
| `AnthropicMessages` | Anthropic | `messages` + `system` separate | SSE with typed events |
| `GeminiGenerate` | Google Gemini | `contents` array | SSE `generateContent` |

The runtime automatically selects the correct driver based on the manifest's `api_style` declaration.

### MCP Tool Integration

AI-Protocol includes a built-in **MCP (Model Context Protocol) tool bridge**. Rather than operating at a separate layer, MCP tools are first-class citizens:

- **McpToolBridge** converts MCP server tools to AI-Protocol `ToolDefinition` format
- Tools are namespaced as `mcp__{server}__{tool_name}` to prevent collisions
- Allow/deny filters control which MCP tools are exposed
- Provider-specific MCP configuration (tool_parameter vs sdk_config) is handled automatically
- Supports stdio, SSE, and streamable HTTP transports

### Computer Use Abstraction

A unified Computer Use capability normalizes GUI automation across providers:

- **ComputerAction** enum covers all action types: screenshot, mouse click, keyboard type, browser navigate, file read/write
- **SafetyPolicy** enforces mandatory safety constraints loaded from the manifest:
  - Confirmation required for destructive actions
  - Domain allowlist for browser navigation
  - Sensitive path protection
  - Maximum actions per turn limit
  - Sandbox mode support
- Supports both `screen_based` (Anthropic, OpenAI) and `tool_based` (Google) implementation styles

### Extended Multimodal

V2 extends multimodal support beyond vision to include audio, video, and omni-mode:

| Modality | Input | Output | Providers |
|----------|-------|--------|-----------|
| Text | ✅ | ✅ | All |
| Image | ✅ | ✅ (select) | OpenAI, Anthropic, Gemini, Qwen |
| Audio | ✅ | ✅ (select) | OpenAI (STT/TTS), Gemini, Qwen (omni) |
| Video | ✅ | — | Gemini |
| Rerank | — | ✅ | Cohere, Jina |

The **MultimodalCapabilities** module validates content modalities against provider declarations before sending requests.

### CLI Tool

The `ai-protocol-cli` tool provides developer utilities:

```bash
ai-protocol-cli validate <path>        # Validate manifests against schemas
ai-protocol-cli info <provider>         # Show provider capabilities
ai-protocol-cli list                    # List all providers (37 total)
ai-protocol-cli check-compat <manifest> # Check runtime compatibility
```

### Cross-Runtime Consistency

The **compliance test suite** now includes 230+ tests across both runtimes, with 12 dedicated V2 integration tests (6 per runtime) that validate the full chain from manifest loading through MCP bridging, Computer Use safety, and multimodal validation.

## Next Steps

- **[AI-Protocol Overview](/protocol/overview/)** — Deep dive into the specification
- **[Rust SDK](/rust/overview/)** — Explore the Rust runtime
- **[Python SDK](/python/overview/)** — Explore the Python runtime
