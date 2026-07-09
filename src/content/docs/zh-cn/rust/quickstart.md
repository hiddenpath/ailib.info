---
title: Rust Quick Start
description: Get up and running with ai-lib-rust 1.0.1 in minutes.
---

# Rust Quick Start

Examples below match the [`basic_usage`](https://github.com/ailib-official/ai-lib-rust/blob/main/crates/ai-lib-rust/examples/basic_usage.rs) example in the repository.

## Installation

```toml
[dependencies]
ai-lib-rust = "1.0.1"
tokio = { version = "1", features = ["full"] }
futures = "0.3"   # only needed for streaming
```

Optional capabilities:

```toml
ai-lib-rust = { version = "1.0.1", features = ["embeddings", "telemetry"] }
# or features = ["full"]
```

## API key

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## Basic chat

```rust
use ai_lib_rust::{AiClient, Message};

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("deepseek/deepseek-chat").await?;

    let response = client
        .chat()
        .messages(vec![
            Message::system("You are a helpful assistant."),
            Message::user("Explain quantum computing in simple terms."),
        ])
        .temperature(0.7)
        .max_tokens(500)
        .execute()
        .await?;

    println!("{}", response.content);
    Ok(())
}
```

## Streaming

Event variant is **`PartialContentDelta`** (not `ContentDelta`):

```rust
use ai_lib_rust::{AiClient, Message, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("deepseek/deepseek-chat").await?;

    let mut stream = client
        .chat()
        .messages(vec![Message::user("Write a haiku about Rust.")])
        .stream()
        .execute_stream()
        .await?;

    while let Some(event) = stream.next().await {
        match event? {
            StreamingEvent::PartialContentDelta { content, .. } => print!("{content}"),
            StreamingEvent::StreamEnd { .. } => break,
            _ => {}
        }
    }
    Ok(())
}
```

## Tool calling (streaming)

```rust
use ai_lib_rust::{AiClient, Message, StreamingEvent, ToolDefinition};
use futures::StreamExt;
use serde_json::json;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("openai/gpt-4o").await?;

    let weather_tool = ToolDefinition {
        name: "get_weather".into(),
        description: Some("Get current weather".into()),
        parameters: json!({
            "type": "object",
            "properties": { "city": { "type": "string" } },
            "required": ["city"]
        }),
    };

    let mut stream = client
        .chat()
        .messages(vec![Message::user("What's the weather in Tokyo?")])
        .tools(vec![weather_tool])
        .stream()
        .execute_stream()
        .await?;

    while let Some(event) = stream.next().await {
        match event? {
            StreamingEvent::ToolCallStarted { tool_name, .. } => {
                println!("Calling: {tool_name}");
            }
            StreamingEvent::PartialToolCall { arguments, .. } => print!("{arguments}"),
            StreamingEvent::PartialContentDelta { content, .. } => print!("{content}"),
            _ => {}
        }
    }
    Ok(())
}
```

## Share `AiClient` across tasks

```rust
use ai_lib_rust::AiClient;
use std::sync::Arc;

let client = Arc::new(AiClient::new("openai/gpt-4o").await?);
```

## Protocol manifests

Set a local checkout of [ai-protocol](https://github.com/ailib-official/ai-protocol):

```bash
export AI_PROTOCOL_DIR="/path/to/ai-protocol"
```

Or pass a base path in code:

```rust
use ai_lib_rust::protocol::ProtocolLoader;

let loader = ProtocolLoader::new().with_base_path("./ai-protocol");
let manifest = loader.load_provider("openai").await?;
```

## Run the shipped example

```bash
cd ai-lib-rust
DEEPSEEK_API_KEY=your_key cargo run --example basic_usage
```

## Next steps

- **[Overview](/rust/overview/)** — architecture & feature boundaries
- **[Client API](/rust/client/)** — builder reference
- **[Streaming](/rust/streaming/)** — pipeline operators
- **[Resilience](/rust/resilience/)** — opt-in policy layer
