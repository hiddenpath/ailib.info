---
title: Circuit Breaker
group: Reliability
order: 60
status: partial
---

# Circuit Breaker (Partial)

Opens after failure threshold; half-open allows limited trial calls before fully closing. Current scope likely coarse (provider/model level).

```rust
// let cb = CircuitBreaker::new().failures(5).window(Duration::from_secs(30)).cooldown(Duration::from_secs(10));
// let client = AiClientBuilder::new(Provider::OpenAI).circuit_breaker(cb).build()?;
```

Planned: error weighting and finer granularity per endpoint.
