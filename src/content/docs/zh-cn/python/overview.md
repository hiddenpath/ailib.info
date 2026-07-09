---
title: Python SDK Overview
description: Architecture and public API of ai-lib-python v1.0.0 — the async Python runtime for AI-Protocol.
---

# Python SDK Overview

**ai-lib-python** (v1.0.0) is the Python runtime for [AI-Protocol](https://github.com/ailib-official/ai-protocol). Unlike Rust’s workspace crates, Python ships as **one package** with clear **execution / policy module separation**:

| Layer | Modules | Role |
|-------|---------|------|
| Execution (E) | `client`, `protocol`, `pipeline`, `transport`, `types`, `structured`, optional capability modules | Manifest loading, operator pipeline, httpx transport |
| Policy (P) | `resilience`, `cache`, `routing`, `plugins`, `guardrails`, `batch`, `telemetry`, `tokens` | Retry, rate limits, routing — opt-in beside the client |

## Primary execution path

For chat, **`AiClient` does not call `ProviderDriver`**. It:

1. Loads a provider manifest (`ProtocolLoader`)
2. Builds a **`Pipeline`** from manifest operators
3. Sends HTTP via **`HttpTransport`** (httpx)
4. Emits unified **`StreamingEvent`** values (Pydantic models)

Provider-specific logic still exists (SSE decoders, optional drivers, standalone service clients), but the default integration path is manifest + pipeline.

## Public API at a glance

**Always exported from `ai_lib_python`:**

- `AiClient`, `AiClientBuilder`, `ChatResponse`, `CallStats`
- `Message`, `MessageRole`, `MessageContent`, `ContentBlock`, `StreamingEvent`, `ToolCall`, `ToolDefinition`
- `AiLibError`, `ProtocolError`, `TransportError`
- Feature probes: `HAS_VISION`, `HAS_AUDIO`, `HAS_TELEMETRY`, `HAS_TOKENIZER`, `HAS_WATCHDOG`, `HAS_KEYRING`, `require_extra`

**Import subpackages explicitly** when needed: `resilience`, `structured`, `embeddings`, `mcp`, `computer_use`, `drivers`, etc.

## V2 alignment (what is real today)

- **Manifest loading:** V1 + V2 paths (`dist/v2/providers/*.json`, `v2/providers/*.yaml`, …)
- **Standard error codes:** 13 codes (E1001–E9999)
- **Structured output:** `structured` module
- **Text-tool / TTC:** types under `ai_lib_python.types.text_tool`
- **Capability registry:** `registry.CapabilityRegistry` with pip-extra detection

### Honest capability boundaries

| Area | In the package | Not included |
|------|----------------|--------------|
| **MCP** | `McpToolBridge` format conversion | MCP server transport wired into `AiClient` |
| **Computer Use** | `ComputerAction`, `SafetyPolicy` validation | Screenshot / input execution environment |
| **Embeddings / STT / TTS / Rerank** | Standalone HTTP clients | Full pipeline operators for every modality |
| **Hot reload** | Builder flag + in-memory cache | Automatic file watching (needs `watchdog`; not wired end-to-end) |
| **`ProviderDriver`** | Public `drivers` module | Default `AiClient` chat path |

## Architecture (package layout)

### Client (`client/`)

- `AiClient` — async entry point (`await AiClient.create("provider/model")`)
- `ChatRequestBuilder` — `.messages()`, `.system()`, `.user()`, `.stream()`, `.execute()`, `.execute_with_stats()`
- `AiClientBuilder` — `.production_ready()`, `.hot_reload()`, resilience knobs

### Protocol (`protocol/`)

- `ProtocolLoader`, `ProtocolManifest`, validators
- V2 types under `protocol.v2`

### Pipeline (`pipeline/`)

Decoder → Selector → Accumulator → FanOut → EventMapper (configured from manifests).

### Transport (`transport/`)

`HttpTransport`, credential resolution (`keyring` or `<PROVIDER>_API_KEY`).

### Policy (`resilience/`, `routing/`, …)

Opt-in modules — use `AiClientBuilder.production_ready()` or wire `ResilientConfig` explicitly; not auto-enabled by `AiClient.create()`.

## Pip extras

| Extra | Enables |
|-------|---------|
| `vision` / `audio` | Multimodal helpers (`HAS_VISION`, `HAS_AUDIO`) |
| `embeddings` | `EmbeddingClient` |
| `stt` / `tts` / `reranking` | Standalone service clients |
| `batch` | Batch collector / executor |
| `telemetry` | OpenTelemetry integration |
| `tokenizer` | tiktoken-based counting |
| `full` | All optional capabilities + `watchdog`, `keyring` |

```bash
pip install ai-lib-python[full]
```

## Next steps

- [Quick Start](/python/quickstart/) — install and first chat
- [AiClient API](/python/client/) — builder reference
- [Streaming](/python/streaming/) — event handling
- [Resilience](/python/resilience/) — opt-in policy layer
