---
title: Core Concepts
group: Guide
order: 10
description: Fundamental abstractions in the Rust crate.
---

# Core Concepts

## Message Abstraction
`Message` (in `types::common`) unifies roles (`Role::User`, `Role::Assistant`, etc.) and content variants via the `Content` enum (text and potentially other modalities).

## Provider & Model Metadata
`Provider` enum selects a backend. Model metadata & selection strategies live in `provider::models` (e.g. capabilities, pricing, performance tiers).

## Tool / Function Calls
If enabled, structured tool calls surface via response inspection—execute externally and supply another message. (Confirm current API in docs.rs.)

## Reliability Primitives
Retry, fallback, race (hedging), and routing strategies are being iteratively integrated. Circuit breaker & advanced rate limiting are partial.

## Streaming
Streaming (if a provider supports it) yields incremental `ChatCompletionChunk` items. Aggregate their deltas into a final answer string.
