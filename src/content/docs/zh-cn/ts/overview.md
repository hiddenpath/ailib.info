---
title: TypeScript SDK Overview
description: Architecture and public API of ai-lib-ts v1.0.0 — the TypeScript runtime for AI-Protocol.
---

# TypeScript SDK Overview

**ai-lib-ts** (v1.0.0) is the TypeScript / Node.js runtime for [AI-Protocol](https://github.com/ailib-official/ai-protocol). Published as `@ailib-official/ai-lib-ts` with three entry points:

| Import | Layer | Use when |
|--------|-------|----------|
| `@ailib-official/ai-lib-ts` | E + P facade | Full SDK (default) |
| `@ailib-official/ai-lib-ts/core` | Execution only | Minimal bundle — no policy transport wrapper |
| `@ailib-official/ai-lib-ts/contact` | Policy only | Resilience, routing — no `AiClient` |

## Primary execution path

For chat, **`AiClient` does not use the low-level `Pipeline` operator API**. It:

1. Loads a provider manifest
2. Builds HTTP requests from manifest fields
3. Sends via **`HttpTransport`**
4. Parses JSON / SSE with manifest `response_paths` and OpenAI-style fallbacks

`Pipeline` remains public for compliance tests and advanced integrations. There is **no** `ProviderDriver` in this runtime.

## Public API at a glance

**Package root exports:**

- `AiClient`, `AiClientBuilder`, `createClient`, `createClientBuilder`
- `Message`, `StreamingEvent`, `Tool`, execution metadata types
- `ProtocolLoader`, manifest + V2 types
- Policy: `RetryPolicy`, `CircuitBreaker`, `RateLimiter`, `ModelManager`, `FallbackChain`, …
- Extras: `EmbeddingClient`, `McpToolBridge`, `Guardrails`, telemetry helpers

### Honest capability boundaries

| Area | In the package | Not included |
|------|----------------|--------------|
| **MCP** | `McpToolBridge` conversion | MCP server transport in `AiClient` |
| **Computer Use** | V2 config types | Runtime executor |
| **Hot reload** | — | Not implemented |
| **Resilience** | Manifest retry on default transport | CB / rate limit / backpressure unless configured on transport |
| **Embeddings** | `EmbeddingClient` | Manifest pipeline path |

## Next steps

- [Quick Start](/ts/quickstart/)
- [Streaming](/ts/streaming/)
- [Resilience](/ts/resilience/)
