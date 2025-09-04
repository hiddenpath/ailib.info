---
title: FAQ
group: Overview
order: 90
---

# FAQ

## Is this production ready?
Core abstractions (client, request/response types) are usable. Reliability primitives (retry / fallback / race / routing) are a focus; rate limiting & circuit breaker partial.

## Why not call providers directly?
One unified Rust API reduces per-provider code paths and enables cross-provider reliability strategies.

## Which language bindings?
Currently Rust (crate). Other language wrappers may appear later; follow the repository roadmap.
