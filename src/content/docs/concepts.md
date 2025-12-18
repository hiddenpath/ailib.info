---
title: Core Concepts
group: Guide
order: 10
description: Fundamental abstractions in the Rust crate.
---

# Core Concepts

Understanding these core concepts will help you effectively use ai-lib in your applications.

## Message Abstraction

The `Message` struct unifies conversation roles and content across all providers:

```rust
use ai_lib::{Message, Role, Content};

// Create a user message with text content (convenience method)
let user_msg = Message::user("Hello, world!");

// Or use custom content (images, audio, etc.)
let user_msg_with_content = Message::user_with_content(Content::new_text("Hello, world!"));

// Create a system message
let system_msg = Message::system("You are a helpful assistant.");
```

The `Content` enum supports multiple modalities:
- **Text**: Plain text content
- **Image**: Image references with URL, MIME type, and optional name
- **Audio**: Audio content with URL and MIME type
- **Json**: Structured JSON data for function calls

## ChatProvider Trait

The `ChatProvider` trait is the core abstraction that all providers implement. It defines the standard interface for:
- `chat`: Unary chat completion
- `stream`: Streaming chat completion
- `batch`: Batch processing
- `list_models`: Fetching available models
- `get_model_info`: Retrieving model details

## Provider & Model Management

The `Provider` enum selects your AI backend:

```rust
use ai_lib::{Provider, AiClient};

// Supported providers
let groq = AiClient::new(Provider::Groq)?;
let openai = AiClient::new(Provider::OpenAI)?;
let anthropic = AiClient::new(Provider::Anthropic)?;
```

Model metadata and selection strategies are managed through:
- **ModelArray**: Groups of models with load balancing
- **ModelSelectionStrategy**: Performance, cost, or health-based selection
- **LoadBalancingStrategy**: Round-robin, weighted, or health-based distribution

## Function Calling

ai-lib provides unified function calling across all providers:

```rust
use ai_lib::{Tool, FunctionCallPolicy, FunctionCall};

// Define a tool
let weather_tool = Tool::new_json(
    "get_weather",
    Some("Get current weather information"),
    serde_json::json!({
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    })
);

// Use in request
let req = ChatCompletionRequest::new(model, messages)
    .with_functions(vec![weather_tool])
    .with_function_call(FunctionCallPolicy::Auto);
```

## Reliability Primitives

Built-in reliability features include:

- **Retry Logic**: Exponential backoff with error classification
- **Circuit Breaker**: Automatic failure detection and recovery
- **Rate Limiting**: Token bucket algorithm for request throttling
- **Fallback Strategies**: Multi-provider failover
- **Health Monitoring**: Endpoint health tracking and avoidance

## Streaming

Consistent streaming across all providers:

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

## Configuration Patterns

ai-lib supports progressive configuration complexity:

1. **Environment Variables**: Automatic provider key detection
2. **Builder Pattern**: Explicit configuration with `AiClientBuilder`
3. **Connection Options**: Runtime overrides for proxy, timeout, etc.
4. **Custom Transport**: Pluggable HTTP transport implementation
5. **Custom Metrics**: Observability integration points

## Error Handling

Comprehensive error classification:

```rust
match client.chat_completion(req).await {
    Ok(response) => println!("Success: {}", response.first_text()?),
    Err(e) if e.is_retryable() => {
        // Handle retryable errors (network, rate limits)
        println!("Retryable error: {}", e);
    }
    Err(e) => {
        // Handle permanent errors (auth, invalid request)
        println!("Permanent error: {}", e);
    }
}
```
