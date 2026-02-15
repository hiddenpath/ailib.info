---
title: Chat Completions
description: Guide to using chat completions across providers with AI-Lib runtimes.
---

# Chat Completions

Chat completions are the primary API for interacting with AI models. Both runtimes provide a unified interface that works across all 35+ providers.

## Basic Usage

### Rust

```rust
let client = AiClient::new("openai/gpt-4o").await?;

let response = client.chat()
    .user("Hello, world!")
    .execute()
    .await?;

println!("{}", response.content);
```

### Python

```python
client = await AiClient.create("openai/gpt-4o")

response = await client.chat() \
    .user("Hello, world!") \
    .execute()

print(response.content)
```

## Messages

### System Messages

Set the model's behavior:

```rust
// Rust
client.chat()
    .system("You are a helpful coding assistant. Always include code examples.")
    .user("Explain closures")
    .execute().await?;
```

```python
# Python
await client.chat() \
    .system("You are a helpful coding assistant.") \
    .user("Explain closures") \
    .execute()
```

### Multi-turn Conversations

Pass conversation history:

```rust
// Rust
use ai_lib::{Message, MessageRole};

let messages = vec![
    Message::system("You are a tutor."),
    Message::user("What is recursion?"),
    Message::assistant("Recursion is when a function calls itself..."),
    Message::user("Can you show an example?"),
];

client.chat().messages(messages).execute().await?;
```

```python
# Python
from ai_lib_python import Message

messages = [
    Message.system("You are a tutor."),
    Message.user("What is recursion?"),
    Message.assistant("Recursion is when a function calls itself..."),
    Message.user("Can you show an example?"),
]

await client.chat().messages(messages).execute()
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | float | Randomness (0.0 = deterministic, 2.0 = creative) |
| `max_tokens` | int | Maximum response length |
| `top_p` | float | Nucleus sampling (alternative to temperature) |
| `stop` | string[] | Sequences that stop generation |

```rust
// Rust
client.chat()
    .user("Write a poem")
    .temperature(0.9)
    .max_tokens(200)
    .top_p(0.95)
    .execute().await?;
```

## Streaming

For real-time output, use streaming:

```rust
// Rust
let mut stream = client.chat()
    .user("Tell me a story")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    if let StreamingEvent::ContentDelta { text, .. } = event? {
        print!("{text}");
        std::io::stdout().flush()?;
    }
}
```

```python
# Python
async for event in client.chat() \
    .user("Tell me a story") \
    .stream():
    if event.is_content_delta:
        print(event.as_content_delta.text, end="", flush=True)
```

## Response Statistics

Track usage for cost management:

```rust
// Rust
let (response, stats) = client.chat()
    .user("Hello")
    .execute_with_stats()
    .await?;

println!("Prompt tokens: {}", stats.prompt_tokens);
println!("Completion tokens: {}", stats.completion_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

```python
# Python
response, stats = await client.chat() \
    .user("Hello") \
    .execute_with_stats()

print(f"Tokens: {stats.total_tokens}")
print(f"Latency: {stats.latency_ms}ms")
```

## Provider Switching

The same code works across all providers:

```rust
// Just change the model identifier
let client = AiClient::new("anthropic/claude-3-5-sonnet").await?;
let client = AiClient::new("deepseek/deepseek-chat").await?;
let client = AiClient::new("gemini/gemini-2.0-flash").await?;
```

The protocol manifest handles endpoint URLs, authentication, parameter mapping, and streaming format differences automatically.
