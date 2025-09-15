---
title: Fallback Chains
group: Reliability
order: 20
status: stable
---

# Fallback Chains (Stable)

Define an ordered list of models/providers. On error or policy match, advance to the next. Pseudocode:

```rust
// let chain = FallbackChain::new()
//     .primary("gpt-4o")
//     .on_timeout("claude-3-haiku")
//     .always("mistral-medium");
// let client = AiClientBuilder::new(Provider::OpenAI).fallback(chain).build()?;
```

First success short-circuits the chain. Combine with racing for tail latency reduction.

## Basic Failover (OSS)

`AiClient::with_failover(Vec<Provider>)` provides lightweight provider-level failover: when retryable errors occur (network, timeout, rate limit, 5xx), it attempts fallback providers in sequence. When used with `routing_mvp`, the selected model is preserved during failover.

```rust
use ai_lib::{AiClient, Provider};

let client = AiClient::new(Provider::OpenAI)?
    .with_failover(vec![Provider::Anthropic, Provider::Groq]);
```

> Note: Advanced weighted/cost and SLO-aware strategies are available in `ai-lib-pro`.
