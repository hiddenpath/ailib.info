---
title: Features & Optional Modules
group: Overview
order: 15
status: stable
---

# Features & Optional Modules

This guide explains how to include `ai-lib` in your Cargo project with opt-in features, along with recommended presets for different scenarios.

## Basic Dependency

```toml
[dependencies]
ai-lib = "0.3.3"
tokio = { version = "1", features = ["full"] }
```

## Enabling Features

`ai-lib` ships lean-by-default. Turn on features as needed:

```toml
[dependencies]
ai-lib = { version = "0.3.3", features = ["resilience", "streaming"] }
```

### Feature Aliases (for ergonomics)

- resilience → enables `interceptors` (retry, rate-limit, circuit-breaker wiring)
- streaming → enables `unified_sse` (unified streaming parser)
- transport → enables `unified_transport` (shared reqwest client factory)
- hot_reload → enables `config_hot_reload` (config provider/watch traits)
- all → turns on most OSS features: `interceptors`, `unified_transport`, `unified_sse`, `cost_metrics`, `routing_mvp`, `observability`, `config_hot_reload`

These aliases are additive; they do not add new code, only enable existing granular features.

## Suggested Combos

- Minimal app: no features (add only when needed)
- Production app: `resilience`, `transport`, `streaming`
- Advanced ops: `resilience`, `transport`, `streaming`, `observability`
- Dynamic config: add `hot_reload`

## Example: Production-lean Setup

```toml
[dependencies]
ai-lib = { version = "0.3.3", features = [
  "resilience",
  "transport",
  "streaming"
] }
```

## Import Style

Prefer root imports for developer ergonomics:

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role, Content};
use ai_lib::{Tool, FunctionCallPolicy};
```

## Notes

- Keep your dependency surface minimal: enable only what you use.
- Features are forward-compatible; we avoid breaking renames.
- See also: [Getting Started](/docs/getting-started), [Chat & Streaming](/docs/chat).


