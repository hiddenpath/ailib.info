---
title: Resilience (Rust)
description: Production reliability patterns in ai-lib-rust v0.8.0 — circuit breaker, rate limiter, backpressure, retry.
---

# Resilience Patterns

ai-lib-rust (v0.8.0) includes production-grade reliability patterns out of the box. Retry and fallback decisions use V2 standard error codes: the `retryable` and `fallbackable` properties on `StandardErrorCode` determine whether an error triggers retries or model fallback.

## Circuit Breaker

Prevents cascading failures by stopping requests to failing providers:

**States:**
- **Closed** — Normal operation, requests flow through
- **Open** — Too many failures, requests immediately rejected
- **Half-Open** — After cooldown, allows a test request

**Configuration:**

```bash
export AI_LIB_BREAKER_FAILURE_THRESHOLD=5
export AI_LIB_BREAKER_COOLDOWN_SECS=30
```

The circuit opens after `FAILURE_THRESHOLD` consecutive failures and stays open for `COOLDOWN_SECS` before testing.

## Rate Limiter

Token bucket algorithm prevents exceeding provider rate limits:

```bash
export AI_LIB_RPS=10    # Max requests per second
export AI_LIB_RPM=600   # Max requests per minute
```

Requests beyond the limit are queued rather than rejected, providing smooth throughput.

## Backpressure

Limits concurrent in-flight requests with a semaphore:

```bash
export AI_LIB_MAX_INFLIGHT=50
```

When the limit is reached, new requests wait until a slot opens.

## Retry

Exponential backoff retry driven by the protocol manifest's retry policy:

```yaml
# In the provider manifest
retry_policy:
  strategy: "exponential_backoff"
  max_retries: 3
  initial_delay_ms: 1000
  max_delay_ms: 30000
  retryable_errors:
    - "rate_limited"
    - "overloaded"
    - "server_error"
```

Only errors classified as retryable trigger retries. Authentication errors, for example, fail immediately.

## Combining Patterns

All resilience patterns work together. A typical request flow:

1. **Backpressure** — Wait for a slot if at max inflight
2. **Circuit Breaker** — Reject immediately if circuit is open
3. **Rate Limiter** — Wait for a token if rate limited
4. **Execute** — Send the request
5. **Retry** — If retryable error, wait and retry
6. **Update** — Record success/failure for circuit breaker

## Observability

Monitor resilience state at runtime:

```rust
// Check circuit breaker state
let state = client.circuit_state();
println!("Circuit: {:?}", state); // Closed, Open, HalfOpen

// Check current inflight count
let inflight = client.current_inflight();
```

## Next Steps

- **[Advanced Features](/rust/advanced/)** — Embeddings, cache, plugins
- **[AiClient API](/rust/client/)** — Client usage
