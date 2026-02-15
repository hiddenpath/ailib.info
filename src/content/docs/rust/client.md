---
title: AiClient API (Rust)
description: Detailed guide to using AiClient, ChatRequestBuilder, and response types in ai-lib-rust v0.7.1.
---

# AiClient API

## Creating a Client

### From Model Identifier

```rust
// Automatic protocol loading
let client = AiClient::from_model("anthropic/claude-3-5-sonnet").await?;
```

### With Builder

```rust
let client = AiClient::builder()
    .model("openai/gpt-4o")
    .protocol_dir("./ai-protocol")
    .timeout(Duration::from_secs(60))
    .build()
    .await?;
```

## ChatRequestBuilder

The builder pattern provides a fluent API:

```rust
let response = client.chat()
    // Messages
    .system("You are a helpful assistant")
    .user("Hello!")
    .messages(vec![Message::user("Follow-up")])

    // Parameters
    .temperature(0.7)
    .max_tokens(1000)
    .top_p(0.9)
    .stop(vec!["END".into()])

    // Tools
    .tools(vec![weather_tool])
    .tool_choice("auto")

    // Execution
    .execute()
    .await?;
```

## Response Types

### ChatResponse

```rust
pub struct ChatResponse {
    pub content: String,         // Response text
    pub tool_calls: Vec<ToolCall>, // Function calls (if any)
    pub finish_reason: String,    // Why the response ended
    pub usage: Usage,             // Token usage
}
```

### StreamingEvent

```rust
pub enum StreamingEvent {
    ContentDelta { text: String, index: usize },
    ThinkingDelta { text: String },
    ToolCallStarted { id: String, name: String, index: usize },
    PartialToolCall { id: String, arguments: String, index: usize },
    ToolCallEnded { id: String, index: usize },
    StreamEnd { finish_reason: Option<String>, usage: Option<Usage> },
    Metadata { model: Option<String>, usage: Option<Usage> },
}
```

### CallStats

```rust
pub struct CallStats {
    pub total_tokens: u32,
    pub prompt_tokens: u32,
    pub completion_tokens: u32,
    pub latency_ms: u64,
    pub model: String,
    pub provider: String,
}
```

## Execution Modes

### Non-Streaming

```rust
// Simple response
let response = client.chat().user("Hello").execute().await?;

// Response with statistics
let (response, stats) = client.chat().user("Hello").execute_with_stats().await?;
```

### Streaming

```rust
let mut stream = client.chat()
    .user("Hello")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    // Handle each StreamingEvent
}
```

### Stream Cancellation

```rust
let (mut stream, cancel_handle) = client.chat()
    .user("Long task...")
    .stream()
    .execute_stream_cancellable()
    .await?;

// Cancel from another task
tokio::spawn(async move {
    tokio::time::sleep(Duration::from_secs(5)).await;
    cancel_handle.cancel();
});
```

## Error Handling

```rust
use ai_lib::{Error, ErrorContext};

match client.chat().user("Hello").execute().await {
    Ok(response) => println!("{}", response.content),
    Err(Error::Protocol(e)) => eprintln!("Protocol error: {e}"),
    Err(Error::Transport(e)) => eprintln!("HTTP error: {e}"),
    Err(Error::Remote(e)) => {
        eprintln!("Provider error: {}", e.error_type);
        // e.error_type is one of the 13 standard error classes
    }
    Err(e) => eprintln!("Other error: {e}"),
}
```

All errors carry V2 standard error codes via `ErrorContext`. Use `error.context().standard_code` to access the `StandardErrorCode` enum (E1001–E9999) for programmatic handling.

## Next Steps

- **[Streaming Pipeline](/rust/streaming/)** — How the pipeline processes streams
- **[Resilience](/rust/resilience/)** — Reliability patterns
- **[Advanced Features](/rust/advanced/)** — Embeddings, cache, plugins
