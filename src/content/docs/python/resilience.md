---
title: Resilience (Python)
description: Production reliability patterns in ai-lib-python — ResilientExecutor, circuit breaker, rate limiter, fallback.
---

# Resilience Patterns

ai-lib-python includes a comprehensive resilience system centered around the `ResilientExecutor`.

## ResilientExecutor

Combines all reliability patterns into a single executor:

```python
from ai_lib_python.resilience import (
    ResilientConfig, RetryConfig, RateLimiterConfig,
    CircuitBreakerConfig, BackpressureConfig
)

config = ResilientConfig(
    retry=RetryConfig(
        max_retries=3,
        initial_delay=1.0,
        max_delay=30.0,
        backoff_multiplier=2.0,
    ),
    rate_limiter=RateLimiterConfig(
        requests_per_second=10,
    ),
    circuit_breaker=CircuitBreakerConfig(
        failure_threshold=5,
        cooldown_seconds=30,
    ),
    backpressure=BackpressureConfig(
        max_inflight=50,
    ),
)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .resilience(config) \
    .build()
```

## Individual Patterns

### Circuit Breaker

```python
from ai_lib_python.resilience import CircuitBreaker

breaker = CircuitBreaker(
    failure_threshold=5,
    cooldown_seconds=30,
)

# Check state
print(breaker.state)  # "closed", "open", "half_open"
```

### Rate Limiter

Token bucket algorithm:

```python
from ai_lib_python.resilience import RateLimiter

limiter = RateLimiter(
    requests_per_second=10,
    burst_size=20,
)
```

### Backpressure

Concurrency limiting:

```python
from ai_lib_python.resilience import Backpressure

bp = Backpressure(max_inflight=50)
```

### Fallback Chain

Multi-target failover:

```python
from ai_lib_python.resilience import FallbackChain

chain = FallbackChain([
    "openai/gpt-4o",
    "anthropic/claude-3-5-sonnet",
    "deepseek/deepseek-chat",
])
```

## PreflightChecker

Unified gating before request execution:

```python
from ai_lib_python.resilience import PreflightChecker

checker = PreflightChecker()
# Checks circuit state, rate limits, inflight count
# before allowing a request through
```

## SignalsSnapshot

Aggregated runtime state:

```python
signals = client.signals_snapshot()
print(f"Circuit: {signals.circuit_state}")
print(f"Inflight: {signals.current_inflight}")
print(f"Rate remaining: {signals.rate_remaining}")
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `AI_LIB_RPS` | Rate limit (requests per second) |
| `AI_LIB_BREAKER_FAILURE_THRESHOLD` | Circuit breaker threshold |
| `AI_LIB_BREAKER_COOLDOWN_SECS` | Cooldown period |
| `AI_LIB_MAX_INFLIGHT` | Max concurrent requests |

## Next Steps

- **[Advanced Features](/docs/python/advanced/)** — Telemetry, routing, plugins
- **[AiClient API](/docs/python/client/)** — Client usage
