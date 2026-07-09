---
title: Resilience (Python)
description: Production reliability patterns in ai-lib-python v1.0.0 — circuit breaker, rate limiter, backpressure, retry.
---

# Resilience Patterns

ai-lib-python (v1.0.0) separates **built-in client backpressure** from **opt-in policy primitives**:

- **`AiClient`:** optional `max_inflight` backpressure via `AiClientBuilder` or `AI_LIB_MAX_INFLIGHT`.
- **`ai_lib_python.resilience`:** retry policies, token-bucket rate limiter, circuit breaker — **not** wired automatically by `AiClient.create()`; use `production_ready()` or explicit `ResilientConfig` (see `examples/resilience.py`).

Retry and fallback decisions use V2 standard error codes: `retryable` and `fallbackable` metadata on normalized errors.

## Quick enable

```python
client = await (
    AiClient.builder()
    .model("deepseek/deepseek-chat")
    .production_ready()  # ResilientConfig.production()
    .build()
)
```

## Circuit breaker

Prevents cascading failures by stopping requests to failing providers.

**States:** Closed → Open (after failure threshold) → Half-Open (test request after cooldown).

Configure via `ResilientConfig` / builder methods — not via undocumented env vars.

## Rate limiter

Token-bucket rate limiting lives in `ai_lib_python.resilience`. Configure on the builder:

```python
from ai_lib_python.resilience import RateLimitConfig

client = await (
    AiClient.builder()
    .model("openai/gpt-4o")
    .with_rate_limit(RateLimitConfig(requests_per_second=10))
    .build()
)
```

`AI_LIB_RPS` / `AI_LIB_RPM` environment variables are **not** read by the runtime.

## Backpressure

Limits concurrent in-flight requests:

```bash
export AI_LIB_MAX_INFLIGHT=50
```

Or on the builder: `.max_inflight(50)`.

## Retry

Exponential backoff retry driven by manifest `retry_policy` and `ResilientConfig`. Only errors classified as retryable trigger retries.

## Combining patterns

A typical request flow when `production_ready()` is enabled:

1. **Backpressure** — wait for a slot if at max inflight
2. **Circuit breaker** — reject immediately if circuit is open
3. **Rate limiter** — wait for a token if rate limited
4. **Execute** — send the HTTP request via pipeline
5. **Retry** — on retryable errors, backoff and retry
6. **Update** — record success/failure for circuit breaker

## Next steps

- **[Advanced Features](/python/advanced/)** — Telemetry, routing, plugins
- **[AiClient API](/python/client/)** — Client usage
