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

## Strategy Builders (OSS)

Use `RoutingStrategyBuilder` plus provider builders to compose deterministic fallback:

```rust
use ai_lib::provider::{RoutingStrategyBuilder, GroqBuilder, AnthropicBuilder, OpenAiBuilder};

let strategy = RoutingStrategyBuilder::new()
    .with_provider(GroqBuilder::new().build_provider()?)
    .with_provider(AnthropicBuilder::new().build_provider()?)
    .build_failover()?;

let client = OpenAiBuilder::new()
    .with_strategy(Box::new(strategy))
    .build()?;
```

> Need weighted, cost-aware, or policy-driven routing? Upgrade to `ai-lib-pro` for advanced schedulers.
