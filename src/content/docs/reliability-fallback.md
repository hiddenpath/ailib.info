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
