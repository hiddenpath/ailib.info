---
title: Intelligent Routing
group: Reliability
order: 40
status: stable
---

# Intelligent Routing (Stable)

Compose routing strategies with strategy builders for load balancing, failover, and intelligent provider selection.

## Strategy Builders (routing_mvp)

Pre-compose routing strategies before runtime using strategy builders:

```rust
use ai_lib::{AiClientBuilder, ChatCompletionRequest, Message, Provider, Role, Content};

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
    // Round-robin load distribution across providers
    let client = AiClientBuilder::new(Provider::OpenAI)
        .with_round_robin_chain(vec![Provider::Groq, Provider::Mistral])?
        .build()?;

    let req = ChatCompletionRequest::new(
        "gpt-4".to_string(), // Model resolved by selected provider
        vec![Message {
            role: Role::User,
            content: Content::Text("Explain quantum computing".to_string()),
            function_call: None
        }]
    );

    let resp = client.chat_completion(req).await?;
    println!("Response from: {}", resp.model);
    Ok(())
}
```

## Failover Chains

Create ordered failover sequences for high availability:

```rust
use ai_lib::{AiClientBuilder, Provider};

// Primary → Secondary → Tertiary failover chain
let client = AiClientBuilder::new(Provider::OpenAI)
    .with_failover_chain(vec![Provider::Anthropic, Provider::Groq])?
    .build()?;

// If OpenAI fails, automatically tries Anthropic, then Groq
let resp = client.chat_completion(request).await?;
```

## Health Checks & Metrics

Strategy builders include built-in health validation:

- **Endpoint Health**: Validates provider endpoints before selection using base URL probes
- **Automatic Fallback**: Seamlessly switches to healthy providers when failures occur
- **Connection Pooling**: Intelligent connection management across provider chains

### Routing Metrics (routing_mvp feature)

When enabled, comprehensive routing telemetry is collected:

- `routing_mvp.request` - Total routing requests
- `routing_mvp.selected` - Successful provider selections
- `routing_mvp.health_fail` - Health check failures
- `routing_mvp.fallback_default` - Fallback to default provider
- `routing_mvp.no_endpoint` - No healthy endpoints available
- `routing_mvp.strategy_fail` - Strategy composition failures

## Advanced Usage

### Custom Provider Injection

Combine strategy builders with custom OpenAI-compatible providers:

```rust
use ai_lib::provider::builders::CustomProviderBuilder;

let custom_provider = CustomProviderBuilder::new("my-gateway")
    .with_base_url("https://custom.ai.gateway/v1")
    .with_api_key_env("CUSTOM_GATEWAY_KEY")
    .with_default_chat_model("gpt-4-turbo")
    .build_provider()?;

let client = AiClientBuilder::new(Provider::OpenAI)
    .with_strategy(custom_provider)
    .build()?;
```

## Notes

- Strategy builders compose routing logic at client construction time, not runtime
- All providers in a chain must be healthy for optimal performance
- Advanced routing policies (cost-aware, latency-based) available in ai-lib-pro
