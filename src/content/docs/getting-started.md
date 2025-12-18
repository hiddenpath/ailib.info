---
title: Getting Started
group: Overview
order: 20
description: Install and run your first chat call in Rust.
---

# Getting Started

ai-lib provides a unified interface to 17+ AI providers using pure Rust. This guide will get you up and running in minutes.

## Add Dependencies

Add ai-lib to your `Cargo.toml`:

```toml
[dependencies]
ai-lib = "0.4.0"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

## Quick Start

The fastest way to get started is with a simple chat request:

```rust
use ai_lib::prelude::*;

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
    // Select your AI provider
    let client = AiClient::new(Provider::Groq)?;

    // Create a chat request
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message {
            role: Role::User,
            content: Content::Text("Explain transformers in one sentence.".to_string()),
            function_call: None,
        }]
    );

    // Send the request
    let resp = client.chat_completion(req).await?;

    // Get the response text
    println!("Answer: {}", resp.choices[0].message.content.as_text());
    Ok(())
}
```

## Environment Variables

Set your API keys as environment variables:

```bash
# For Groq
export GROQ_API_KEY=your_groq_api_key

# For OpenAI
export OPENAI_API_KEY=your_openai_api_key

# For Anthropic
export ANTHROPIC_API_KEY=your_anthropic_api_key

# For other providers, see the full list in [Providers](/docs/providers)
```

## Streaming Example

For real-time responses, use streaming:

```rust
use futures::StreamExt;

let mut stream = client.chat_completion_stream(req).await?;
while let Some(chunk) = stream.next().await {
    let c = chunk?;
    if let Some(delta) = c.choices[0].delta.content.clone() {
        print!("{delta}");
    }
}
```

## Function Calling

ai-lib supports function calling with a unified interface:

```rust
use ai_lib::{Tool, FunctionCallPolicy};

let tool = Tool {
    name: "get_weather".to_string(),
    description: Some("Get current weather information".to_string()),
    parameters: Some(serde_json::json!({
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    }))
};

let req = ChatCompletionRequest::new(model, messages)
    .with_functions(vec![tool])
    .with_function_call(FunctionCallPolicy::Auto);
```

## Proxy Configuration (Optional)

Configure proxy settings if needed:

```bash
export AI_PROXY_URL=http://proxy.example.com:8080
```

Or set it programmatically:

```rust
use ai_lib::{AiClient, Provider, ConnectionOptions};

let client = AiClient::with_options(
    Provider::Groq,
    ConnectionOptions {
        proxy: Some("http://proxy.example.com:8080".into()),
        ..Default::default()
    }
)?;
```

## Enterprise Features

For production environments and enterprise needs, consider [ai-lib-pro](/docs/enterprise-pro):

- **Advanced Routing**: Policy-driven routing, health monitoring, automatic failover
- **Enterprise Observability**: Structured logging, metrics, distributed tracing
- **Cost Management**: Centralized pricing tables and budget tracking
- **Quota Management**: Tenant/organization quotas and rate limiting
- **Audit & Compliance**: Comprehensive audit trails with redaction
- **Security**: Envelope encryption and key management
- **Configuration**: Hot-reload configuration management

## Next Steps

- **Streaming**: Learn about real-time responses in [Chat & Streaming](/docs/chat)
- **Reliability**: Explore retry, circuit breakers, and fallback strategies in [Reliability Overview](/docs/reliability-overview)
- **Advanced Features**: Check out [Advanced Examples](/docs/advanced-examples)
- **Provider Details**: See all supported providers in [Providers](/docs/providers)
- **Enterprise**: Explore [ai-lib-pro](/docs/enterprise-pro) for advanced enterprise capabilities
