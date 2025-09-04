---
title: Introduction
group: Overview
order: 10
description: Overview of Ailib (Rust unified AI SDK) goals and capabilities.
---

# Introduction

Ailib is a Rust crate providing a unified, reliability-focused multi‑provider AI SDK. Goals:

- Reduce integration cost across providers.
- Improve success rate & tail latency via reliability primitives.
- Offer consistent streaming & tool/function semantics.
- Remain vendor-neutral and extensible.

Key Features:

- Unified chat & (when supported) streaming API
- Function / tool calling (verify status in current version)
- Multimodal content (text + other media) where providers support it
- Reliability primitives: retry, fallback, race/hedging, routing (core focus)
- Partial: rate limiting, circuit breaker
- Planned: advanced observability (metrics + tracing)

Next: Read [Getting Started](/docs/getting-started) then explore [Advanced Examples](/docs/advanced-examples).
