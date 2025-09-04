---
title: Retry
group: Reliability
order: 10
status: stable
---

# Retry (Stable)

Exponential backoff with jitter is the expected approach; check the current crate version for exposed configuration APIs. A typical Rust pattern (pseudocode if not yet stabilized):

```rust
// let policy = RetryPolicy { attempts: 3, base_delay: Duration::from_millis(200), max_delay: Duration::from_secs(2) };
// let client = AiClientBuilder::new(Provider::OpenAI).retry(policy).build()?;
```

Errors commonly retried: network / transient transport issues, HTTP 5xx, rate-limit with retry-after header. Guard side-effecting tool executions with idempotency keys or perform them after model reasoning.
