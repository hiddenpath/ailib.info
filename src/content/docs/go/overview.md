---
title: Go SDK Overview
description: Overview of the ai-lib-go runtime implementation.
---

# ai-lib-go

The Go implementation of the AI-Protocol specification. It provides a high-concurrency, idiomatic Go runtime for interacting with 37+ AI providers using a unified interface.

## Core Capabilities

- **Manifest-Driven**: Reads `v2/providers/*.yaml` directly. No hardcoded logic.
- **Go Native**: Uses Go 1.21+ standard concurrency for high-performance streaming.
- **Resilient**: Context-aware timeouts, automatic retries using `net/http`.
- **Type-Safe**: Maps JSON schemas strictly to Go structs.

## Protocol V2 Support

The Go SDK (v1.0.0) is the Wave-5 stable runtime and implements the core Ring 1/Ring 2 features of the V2 specification:

- HTTP Transport handling (Headers, Auth, Endpoint construction)
- SSE and NDJSON Decoding
- Error Classification mapping
- Streaming Accumulation strategies
- Context-aware cancellation
