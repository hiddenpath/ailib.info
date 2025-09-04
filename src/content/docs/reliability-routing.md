---
title: Intelligent Routing
group: Reliability
order: 40
status: stable
---

# Intelligent Routing (Stable)

Selects provider/model based on capability metadata (speed tier, quality tier, cost) and policy objective.

```rust
// let routing = RoutingPolicy::balanced()
//    .allow(["gpt-4o","claude-3-haiku","mistral-medium"]);
// let client = AiClientBuilder::new(Provider::OpenAI).routing(routing).build()?;
```

Planned: feedback loop ingesting latency / quality metrics to adapt selection.
