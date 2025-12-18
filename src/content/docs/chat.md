---
title: Chat & Streaming
group: Guide
order: 20
status: stable
---

# Chat & Streaming

This section shows core APIs: `chat_completion`, streaming variants, cancellation, batch, quick helpers, and model listing. Always verify against the crate version on docs.rs.

## Basic Chat Completion

### Direct Providers
```rust
use ai_lib::prelude::*;

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
  let client = AiClient::new(Provider::OpenAI)?;
  let req = ChatCompletionRequest::new(
    "gpt-4o".to_string(),
    vec![Message { 
        role: Role::User, 
        content: Content::new_text("Summarize Rust ownership succinctly.".to_string()), 
        function_call: None 
    }]
  );
  let resp = client.chat_completion(req).await?;
  if let Some(first) = resp.choices.first() {
    println!("Answer: {}", first.message.content.as_text());
  }
  Ok(())
}
```

### Gateway Providers
When using gateways like OpenRouter, use `provider/model` format for model names:

```rust
use ai_lib::prelude::*;

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
  let client = AiClient::new(Provider::OpenRouter)?;
  let req = ChatCompletionRequest::new(
    "openai/gpt-4o-mini".to_string(), // Note the provider prefix
    vec![Message { 
        role: Role::User, 
        content: Content::new_text("Summarize Rust ownership succinctly.".to_string()), 
        function_call: None 
    }]
  );
  let resp = client.chat_completion(req).await?;
  if let Some(first) = resp.choices.first() {
    println!("Answer: {}", first.message.content.as_text());
  }
  Ok(())
}
```

## Streaming Tokens

Method assumed: `chat_completion_stream(request)` returning an async stream of `Result<ChatCompletionChunk, AiLibError>`.

```rust
use ai_lib::prelude::*;
use futures::StreamExt; // if using futures stream

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
  let client = AiClient::new(Provider::Groq)?;
  let req = ChatCompletionRequest::new(
    "llama3-8b-8192".to_string(),
    vec![Message { 
        role: Role::User, 
        content: Content::new_text("Stream a haiku about concurrency.".to_string()), 
        function_call: None 
    }]
  );
  let mut stream = client.chat_completion_stream(req).await?;
  while let Some(chunk) = stream.next().await {
    match chunk {
      Ok(c) => {
        if let Some(choice) = c.choices.first() {
            if let Some(content) = &choice.delta.content {
                print!("{}", content);
            }
        }
      }
      Err(e) => { eprintln!("stream error: {e}"); break; }
    }
  }
  Ok(())
}
```

## Streaming + Cancellation

Assumed helper: `chat_completion_stream_with_cancel(req)` → `(impl Stream, CancelHandle)`.

```rust
use ai_lib::prelude::*;
use futures::StreamExt;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
  let client = AiClient::new(Provider::OpenAI)?;
  let req = ChatCompletionRequest::new(
    "gpt-4o".to_string(),
    vec![Message { 
        role: Role::User, 
        content: Content::new_text("Explain borrow checker slowly.".to_string()), 
        function_call: None 
    }]
  );
  let (mut stream, handle) = client.chat_completion_stream_with_cancel(req).await?;
  tokio::select! {
    _ = async {
      while let Some(chunk) = stream.next().await {
        if let Ok(c) = chunk { /* print!("{}", c.delta_text()); */ }
      }
    } => {},
    _ = sleep(Duration::from_millis(400)) => {
      handle.cancel();
      eprintln!("Cancelled after 400ms");
    }
  }
  Ok(())
}
```

## Batch Requests

Two patterns (names assumed):

1. `chat_completion_batch(Vec<ChatCompletionRequest>)` – fire concurrently, return Vec of results.
2. `chat_completion_batch_smart` – may apply internal heuristics/routing.

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::types::common::Content;

fn prompt(p: &str) -> ChatCompletionRequest {
  ChatCompletionRequest::new(
    "gpt-4o".to_string(),
    vec![Message { 
        role: Role::User, 
        content: Content::new_text(p.to_string()), 
        function_call: None 
    }]
  )
}

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
  let client = AiClient::new(Provider::OpenAI)?;
  let batch = vec![prompt("Define RAII"), prompt("One sentence on lifetimes"), prompt("Explain Send vs Sync")];
  let results = client.chat_completion_batch(batch, None).await?;
  for (i, r) in results.iter().enumerate() {
    if let Ok(response) = r {
        if let Some(c) = response.choices.first() { 
            println!("{}: {}", i, c.message.content.as_text()); 
        }
    }
  }
  Ok(())
}
```

If a smarter variant exists:

```rust
// let results = client.chat_completion_batch_smart(batch).await?;
```

## Quick Helpers

Some crates expose ergonomic shortcuts like `quick_chat_text(model, prompt)` returning a `String`.

```rust
// let text = client.quick_chat_text("gpt-4o", "What is ownership?" ).await?;
// println!("{text}");
```

## List Models

```rust
let models = client.list_models().await?;
for model in models { 
    println!("{}", model); 
}
```

## Multimodal Content

ai-lib supports text, image, and audio content:

```rust
use ai_lib::prelude::*;

// Text message
let text_msg = Message {
    role: Role::User,
    content: Content::new_text("Describe this image"),
    function_call: None,
};

// Image message (from file)
let image_msg = Message {
    role: Role::User,
    content: Content::from_image_file("path/to/image.jpg"),
    function_call: None,
};

// Image message (from URL)
let image_url_msg = Message {
    role: Role::User,
    content: Content::new_image(
        Some("https://example.com/image.jpg".to_string()),
        Some("image/jpeg".to_string()),
        Some("image.jpg".to_string()),
    ),
    function_call: None,
};

// Audio message (from file)
let audio_msg = Message {
    role: Role::User,
    content: Content::from_audio_file("path/to/audio.mp3"),
    function_call: None,
};

// Audio message (from URL)
let audio_url_msg = Message {
    role: Role::User,
    content: Content::new_audio(
        Some("https://example.com/audio.mp3".to_string()),
        Some("audio/mpeg".to_string()),
    ),
    function_call: None,
};
```

## Error Handling

Handle different types of errors:

```rust
match client.chat_completion(req).await {
    Ok(response) => {
        if let Some(first) = response.choices.first() {
            println!("Success: {}", first.message.content.as_text());
        }
    }
    Err(e) if e.is_retryable() => {
        // Handle retryable errors (network, rate limits)
        println!("Retryable error: {}", e);
        // Implement retry logic
    }
    Err(e) => {
        // Handle permanent errors (auth, invalid requests)
        println!("Permanent error: {}", e);
    }
}
```

## Performance Optimization

### Connection Pool Configuration

```rust
use ai_lib::{AiClient, Provider, ConnectionOptions};
use std::time::Duration;

let client = AiClient::with_options(
    Provider::Groq,
    ConnectionOptions {
        // Configure timeout
        timeout: Some(Duration::from_secs(30)),
        // Set custom proxy
        proxy: Some("http://proxy.example.com:8080".to_string()),
        ..Default::default()
    }
)?;
```

### Concurrency Control

```rust
use tokio::sync::Semaphore;

let semaphore = Arc::new(Semaphore::new(10)); // Limit concurrency to 10

for request in requests {
    let permit = semaphore.clone().acquire_owned().await?;
    let client = client.clone();
    
    tokio::spawn(async move {
        let _permit = permit;
        let result = client.chat_completion(request).await;
        // Handle result
    });
}
```

## Notes

Tips:

- Check docs.rs for any renames (e.g. `chat` vs `chat_completion`).
- Collect streaming deltas into a `String` if you need the final answer.
- Batch + streaming together? Launch multiple `chat_completion_stream` tasks and aggregate.
- More patterns: [Advanced Examples](/docs/advanced-examples)
