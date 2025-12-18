---
title: Fallback Chains
group: Reliability
order: 20
status: stable
---

# Fallback Chains (Stable)

Define ordered failover sequences that automatically advance to the next provider on failure. First success short-circuits the chain.

## Strategy Builders (OSS)

Compose deterministic failover chains at build time:

```rust
use ai_lib::{AiClientBuilder, Provider};

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
    // Primary → Secondary → Tertiary failover chain
    let client = AiClientBuilder::new(Provider::OpenAI)
        .with_failover_chain(vec![Provider::Anthropic, Provider::Groq])?
        .build()?;

    let request = ChatCompletionRequest::new(
        "gpt-4".to_string(),
        vec![Message::user("Explain quantum computing")]
    );

    // Automatically tries OpenAI, then Anthropic, then Groq on failures
    let response = client.chat_completion(request).await?;
    println!("Response: {}", response.choices[0].message.content.as_text());
    Ok(())
}
```

## Behavior

- **Ordered Execution**: Providers tried in the order specified
- **Short-Circuit**: First successful response returns immediately
- **Error Propagation**: Only returns error if all providers in chain fail
- **Health Validation**: Unhealthy providers are skipped automatically

## Advanced Usage

Combine with custom providers for complete control:

```rust
use ai_lib::provider::builders::CustomProviderBuilder;

// Mix standard providers with custom endpoints
let custom = CustomProviderBuilder::new("backup-gateway")
    .with_base_url("https://backup.ai.gateway/v1")
    .with_api_key_env("BACKUP_API_KEY")
    .build_provider()?;

let client = AiClientBuilder::new(Provider::OpenAI)
    .with_strategy(custom)
    .with_failover_chain(vec![Provider::Anthropic])?
    .build()?;
```

> Need weighted, cost-aware, or policy-driven routing? Upgrade to `ai-lib-pro` for advanced schedulers.
