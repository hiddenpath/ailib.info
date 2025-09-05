---
title: Rate Limiting
group: Reliability
order: 50
status: partial
---

# Rate Limiting (Partial)

Token bucket (in-memory) per provider key concept for smoothing bursts.

```rust
// let limiter = RateLimit::per_minute(3000).burst(600);
// let client = AiClientBuilder::new(Provider::OpenAI).rate_limit(limiter).build()?;
```

Adaptive concurrency is implemented. Distributed state is planned for future releases.
