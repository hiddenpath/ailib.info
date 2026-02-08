---
title: Rust Quick Start
description: Get up and running with ai-lib-rust in minutes.
---

# Rust Quick Start

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
ai-lib = "0.6.6"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

## Set API Key

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## Basic Chat

```rust
use ai_lib::{AiClient, Message};

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    let client = AiClient::from_model("deepseek/deepseek-chat").await?;

    let response = client.chat()
        .user("Explain quantum computing in simple terms")
        .temperature(0.7)
        .max_tokens(500)
        .execute()
        .await?;

    println!("{}", response.content);
    Ok(())
}
```

## Streaming

```rust
use ai_lib::{AiClient, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    let client = AiClient::from_model("deepseek/deepseek-chat").await?;

    let mut stream = client.chat()
        .user("Write a haiku about Rust")
        .stream()
        .execute_stream()
        .await?;

    while let Some(event) = stream.next().await {
        match event? {
            StreamingEvent::ContentDelta { text, .. } => print!("{text}"),
            StreamingEvent::StreamEnd { .. } => println!(),
            _ => {}
        }
    }
    Ok(())
}
```

## Tool Calling

```rust
use ai_lib::{AiClient, ToolDefinition, StreamingEvent};
use serde_json::json;
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    let client = AiClient::from_model("openai/gpt-4o").await?;

    let weather_tool = ToolDefinition {
        name: "get_weather".into(),
        description: Some("Get current weather".into()),
        parameters: json!({
            "type": "object",
            "properties": {
                "city": { "type": "string" }
            },
            "required": ["city"]
        }),
    };

    let mut stream = client.chat()
        .user("What's the weather in Tokyo?")
        .tools(vec![weather_tool])
        .stream()
        .execute_stream()
        .await?;

    while let Some(event) = stream.next().await {
        match event? {
            StreamingEvent::ToolCallStarted { name, .. } =>
                println!("Calling: {name}"),
            StreamingEvent::PartialToolCall { arguments, .. } =>
                print!("{arguments}"),
            StreamingEvent::ContentDelta { text, .. } =>
                print!("{text}"),
            _ => {}
        }
    }
    Ok(())
}
```

## Multi-turn Conversation

```rust
use ai_lib::{AiClient, Message, MessageRole};

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    let client = AiClient::from_model("anthropic/claude-3-5-sonnet").await?;

    let messages = vec![
        Message::system("You are a helpful coding assistant."),
        Message::user("What is a closure in Rust?"),
    ];

    let response = client.chat()
        .messages(messages)
        .execute()
        .await?;

    println!("{}", response.content);
    Ok(())
}
```

## With Stats

```rust
let (response, stats) = client.chat()
    .user("Hello!")
    .execute_with_stats()
    .await?;

println!("Content: {}", response.content);
println!("Total tokens: {}", stats.total_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

## Next Steps

- **[AiClient API](/rust/client/)** — Detailed API reference
- **[Streaming Pipeline](/rust/streaming/)** — How streaming works
- **[Resilience](/rust/resilience/)** — Circuit breaker, rate limiting
- **[Advanced Features](/rust/advanced/)** — Embeddings, cache, plugins
