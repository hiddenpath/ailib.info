---
title: Go SDK Overview
description: Architecture and public API of ai-lib-go v1.0.0.
---

# Go SDK Overview

**ai-lib-go** (v1.0.0, Go 1.21+) is the Go runtime for [AI-Protocol](https://github.com/ailib-official/ai-protocol).

| Package | Layer | Role |
|---------|-------|------|
| `pkg/ailib` | Execution (E) | `Client`, manifest HTTP chat, capability endpoints |
| `pkg/contact` | Policy (P) | `FallbackClient`, circuit-breaker policy |

## Primary execution path

`Client.Chat` → manifest endpoint resolution → JSON HTTP → micro-retry (`internal/resilience`) → `ExecutionMetadata` on response.

Without a manifest, `WithBaseURL` + `WithAPIKey` uses OpenAI-compatible defaults.

Streaming: `ChatStream` → SSE decoder (`openai_sse` by default).

## Capability boundaries

| Area | Reality |
|------|---------|
| MCP / Computer Use | Manifest HTTP routes + capability gate — not full wire clients |
| Circuit breaker | `pkg/contact` only |
| Multimodal | Pass-through `Message.Content` JSON |

## Next steps

- [Quick Start](/go/quickstart/)
- [Streaming](/go/streaming/)
- [Resilience](/go/resilience/)
