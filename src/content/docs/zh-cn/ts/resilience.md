---
title: Resilience (TypeScript)
description: Production reliability patterns in ai-lib-ts v1.0.0.
---

# Resilience Patterns

ai-lib-ts (v1.0.0) applies **manifest-derived retry** on the default P-layer `HttpTransport` used by `AiClient`. Circuit breaker, rate limiting, and backpressure are **not** auto-enabled through `AiClientBuilder` — configure `TransportOptions.resilience` when constructing transport manually, or use `PreflightChecker` beside the client.

## What default `AiClient` includes

| Pattern | Default `AiClient` |
|---------|-------------------|
| Retry (non-stream) | Yes — from manifest / defaults |
| Circuit breaker | No |
| Rate limiter | No |
| Backpressure | No |

## `/core` vs root

`@ailib-official/ai-lib-ts/core` uses E-layer `HttpTransport` with **no retry wrapper**. Use root or `/contact` when you need policy behavior.

## Manual resilience

Import from the policy layer and wire transport options explicitly (see `src/transport/index.ts`). `AiClientBuilder` does not provide `.withCircuitBreaker()` / `.withRateLimiter()` chain methods.

## Next steps

- **[Advanced](/ts/advanced/)**
- **[Client API](/ts/client/)**
