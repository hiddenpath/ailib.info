---
title: Rust SDK Overview
description: Architecture and public API of ai-lib-rust v1.0.1 — the high-performance Rust runtime for AI-Protocol.
---

# Rust SDK Overview

**ai-lib-rust** (v1.0.1) is the Rust runtime for [AI-Protocol](https://github.com/ailib-official/ai-protocol). The published crate is a **facade** over two workspace crates:

| Crate | Role |
|-------|------|
| `ai-lib-core` | Execution: `AiClient`, `pipeline`, `protocol`, `transport`, `types`, `structured` |
| `ai-lib-contact` | Policy: `resilience`, `cache`, `routing`, `plugins`, `guardrails`, `batch`, `telemetry` |

## Primary execution path

For chat, **`AiClient` does not call `ProviderDriver`**. It:

1. Loads a provider manifest (`ProtocolLoader`)
2. Builds a **`Pipeline`** from manifest operators
3. Sends HTTP via **`HttpTransport`**
4. Emits unified **`StreamingEvent`** values

Provider-specific logic still exists (SSE decoders, optional drivers, standalone service clients), but the default integration path is manifest + pipeline.

## Public API at a glance

**Always exported from `ai_lib_rust`:**

- `AiClient`, `AiClientBuilder`, `ChatBatchRequest`, `CancelHandle`, `CallStats`
- `Message`, `MessageRole`, `StreamingEvent`, `ToolCall`
- `StandardErrorCode`, `Error`, `Result`
- `structured` (JSON mode / schema validation)
- Text-tool helpers: `StandardTextToolParser`, `ToolCallingPolicy`, …
- Policy modules: `cache`, `context`, `plugins`, `resilience`

**Feature-gated** (see [Feature flags](#feature-flags)):

- Core: `embeddings`, `mcp`, `computer_use`, `multimodal`, `stt`, `tts`, `rerank`
- Contact: `batch`, `guardrails`, `telemetry`, `tokens`, `routing_mvp`, `interceptors`

## V2 alignment (what is real today)

- **Manifest loading:** V1 + V2 paths (`dist/v2/providers/*.json`, `v2/providers/*.yaml`, …)
- **Standard error codes:** 13-variant `StandardErrorCode` (E1001–E9999)
- **Structured output:** `JsonModeConfig`, `OutputValidator` (always available)
- **Text-tool / TTC:** `StandardTextToolParser` and policy types at crate root
- **Capability registry:** `registry::CapabilityRegistry` (feature-gap detection)

### Honest capability boundaries

| Area | In the crate | Not included |
|------|--------------|--------------|
| **MCP** (`mcp` feature) | `McpToolBridge` format conversion | MCP server transport wired into `AiClient` |
| **Computer Use** (`computer_use`) | `ComputerAction`, `SafetyPolicy` validation | Screenshot / input execution environment |
| **Embeddings / STT / TTS / Rerank** | Standalone HTTP clients | Full pipeline operators for every modality |
| **Hot reload** | Manifest in-memory cache | File watching / automatic reload |
| **`ProviderDriver`** | Public `drivers` module | Default `AiClient` chat path |

## Architecture (workspace paths)

### Client (`crates/ai-lib-core/src/client/`)

- `AiClient` — entry point (`"provider/model"` id)
- `ChatRequestBuilder` — `.messages()`, `.stream()`, `.execute()`, `.execute_stream()`
- `chat_batch` / `chat_batch_smart` — always on `AiClient` (not behind `batch` feature)

### Protocol (`crates/ai-lib-core/src/protocol/`)

- `ProtocolLoader`, `ProtocolManifest`, validators
- V2 types under `protocol::v2`

### Pipeline (`crates/ai-lib-core/src/pipeline/`)

Decoder → Selector → Accumulator → FanOut → EventMapper (configured from manifests).

### Transport (`crates/ai-lib-core/src/transport/`)

`HttpTransport`, credential resolution (`keyring` or `<PROVIDER>_API_KEY`).

### Policy (`crates/ai-lib-contact/src/`)

Opt-in modules — import and wire beside `AiClient`; not auto-enabled by `AiClient::new`.

## Feature flags

| Feature | Enables |
|---------|---------|
| `embeddings` | `EmbeddingClient` |
| `stt` / `tts` / `reranking` | `SttClient`, `TtsClient`, `RerankerClient` |
| `mcp` | `McpToolBridge` |
| `computer_use` | `ComputerAction`, `SafetyPolicy` |
| `multimodal` | `MultimodalCapabilities` |
| `batch` | `BatchExecutor` (contact); `chat_batch` is always available |
| `guardrails` | Content filters |
| `telemetry` | Advanced feedback sinks |
| `routing_mvp` | `CustomModelManager`, `ModelArray` |
| `full` | All of the above |

```toml
ai-lib-rust = { version = "1.0.1", features = ["embeddings"] }
```

## Resilience

- **`AiClient`:** `max_inflight` backpressure (`AI_LIB_MAX_INFLIGHT`)
- **`ai_lib_rust::resilience`:** retry, rate limiter, circuit breaker — configure explicitly
- **Not built into default client:** automatic breaker / rate limit on every `AiClient::new`

## Environment variables

| Variable | Purpose |
|----------|---------|
| `AI_PROTOCOL_DIR` / `AI_PROTOCOL_PATH` | Local or remote manifest root |
| `<PROVIDER>_API_KEY` | API key (e.g. `OPENAI_API_KEY`) |
| `AI_LIB_MAX_INFLIGHT` | Concurrent request cap |
| `AI_LIB_BATCH_CONCURRENCY` | Batch worker count |
| `AI_HTTP_TIMEOUT_SECS` | HTTP timeout |
| `AI_PROXY_URL` | Explicit proxy override |

## Next steps

- **[Quick Start](/rust/quickstart/)** — install and first chat
- **[AiClient API](/rust/client/)** — builder methods
- **[Streaming](/rust/streaming/)** — pipeline & events
- **[Resilience](/rust/resilience/)** — policy layer
- **[Advanced](/rust/advanced/)** — embeddings, cache, plugins

Source of truth: [ai-lib-rust README](https://github.com/ailib-official/ai-lib-rust/blob/main/README.md).
