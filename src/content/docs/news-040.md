---
title: Release v0.4.0
group: News
order: 0
status: stable
---

# ai-lib v0.4.0

**Released: 2025-12-04**

This release marks a major architectural milestone: the **Trait Shift 1.0 Evolution**. The core dispatching mechanism has been redesigned from enum-based to trait-based architecture, providing better extensibility and cleaner abstractions.

## Highlights

- **ChatProvider Trait**: All providers now implement a unified `ChatProvider` trait for consistent behavior
- **Strategy Builders**: Pre-runtime routing composition with `with_failover_chain` and `with_round_robin_chain`
- **Custom Providers**: Inject OpenAI-compatible endpoints without modifying the `Provider` enum
- **Improved Error Handling**: `AiClient::new` now returns `Result<AiClient, AiLibError>` for explicit error handling

## Breaking Changes

### AiClient::new Returns Result

```rust
// ⛔️ Old (0.3.x)
let client = AiClient::new(Provider::Groq);

// ✅ New (0.4.0)
let client = AiClient::new(Provider::Groq)?;
```

### Strategy-Based Routing

```rust
// ⛔️ Old (0.3.x) - Sentinel-based failover
let client = AiClient::new(Provider::OpenAI)
    .with_failover(vec![Provider::Anthropic, Provider::Groq]);

// ✅ New (0.4.0) - Strategy builders
let client = AiClientBuilder::new(Provider::OpenAI)
    .with_failover_chain(vec![Provider::Anthropic, Provider::Groq])?
    .build()?;
```

## New Features

### Custom Provider Injection

```rust
use ai_lib::provider::builders::CustomProviderBuilder;

let custom = CustomProviderBuilder::new("my-gateway")
    .with_base_url("https://gateway.example.com/v1")
    .with_api_key_env("MY_GATEWAY_KEY")
    .with_default_chat_model("gpt-4")
    .build_provider()?;

let client = AiClientBuilder::new(Provider::OpenAI)
    .with_strategy(custom)
    .build()?;
```

### Round-Robin Load Distribution

```rust
let client = AiClientBuilder::new(Provider::OpenAI)
    .with_round_robin_chain(vec![Provider::Groq, Provider::Mistral])?
    .build()?;
```

## Upgrade

```toml
[dependencies]
ai-lib = "0.4.0"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

## Documentation

- [Upgrade Guide](/docs/UPGRADE_0.4.0.md) - Migration from 0.3.x to 0.4.0
- [API Reference](https://docs.rs/ai-lib/0.4.0) - Complete API documentation
- [Examples](https://github.com/hiddenpath/ai-lib/tree/main/examples) - Practical usage examples
