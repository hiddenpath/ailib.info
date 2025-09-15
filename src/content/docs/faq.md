---
title: FAQ
group: Overview
order: 90
---

# FAQ

## Is this production ready?

Yes, ai-lib has reached production readiness (v0.3.4). Core functionality is fully implemented:

- **Complete reliability primitives**: Retry, circuit breaker, rate limiting, timeout control
- **Interceptor system**: Pluggable middleware pipeline with custom interceptor support
- **Multi-provider support**: OpenAI, Google Gemini, Mistral, Cohere, and more
- **Streaming processing**: Complete SSE and JSONL streaming protocol support
- **Function calling**: Cross-provider structured tool calling
- **Multimodal support**: Text, image, and audio processing
- **Enterprise features**: Proxy support, batch processing, metrics monitoring

## Why not call providers directly?

One unified Rust API reduces per-provider code paths and enables cross-provider reliability strategies.

## Which language bindings?

Currently Rust (crate). Other language wrappers may appear later; follow the repository roadmap.
