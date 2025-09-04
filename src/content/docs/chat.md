---
title: Chat & Streaming
group: Guide
order: 20
status: stable
---

# Chat & Streaming

This section shows core APIs: `chat_completion`, streaming variants, cancellation, batch, quick helpers, and model listing. Always verify against the crate version on docs.rs.

## Basic Chat Completion

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::types::common::Content;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
  let client = AiClient::new(Provider::OpenAI)?;
  let req = ChatCompletionRequest::new(
    "gpt-4o".into(),
    vec![Message { role: Role::User, content: Content::Text("Summarize Rust ownership succinctly.".into()), function_call: None }]
  );
  let resp = client.chat_completion(req).await?;
  if let Some(first) = resp.choices.first() {
    // println!("Answer: {}", first.message_text()); // adapt to actual helper
  }
  Ok(())
}
```

## Streaming Tokens

Method assumed: `chat_completion_stream(request)` returning an async stream of `Result<ChatCompletionChunk, AiLibError>`.

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::types::common::Content;
use futures_util::StreamExt; // if using futures stream

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
  let client = AiClient::new(Provider::Groq)?;
  let req = ChatCompletionRequest::new(
    "llama3-8b-8192".into(),
    vec![Message { role: Role::User, content: Content::Text("Stream a haiku about concurrency.".into()), function_call: None }]
  );
  let mut stream = client.chat_completion_stream(req).await?;
  while let Some(chunk) = stream.next().await {
    match chunk {
      Ok(c) => {
        // print!("{}", c.delta_text()); // adapt to actual field accessor
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
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::types::common::Content;
use futures_util::StreamExt;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
  let client = AiClient::new(Provider::OpenAI)?;
  let req = ChatCompletionRequest::new(
    "gpt-4o".into(),
    vec![Message { role: Role::User, content: Content::Text("Explain borrow checker slowly.".into()), function_call: None }]
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
    "gpt-4o".into(),
    vec![Message { role: Role::User, content: Content::Text(p.into()), function_call: None }]
  )
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
  let client = AiClient::new(Provider::OpenAI)?;
  let batch = vec![prompt("Define RAII"), prompt("One sentence on lifetimes"), prompt("Explain Send vs Sync")];
  let results = client.chat_completion_batch(batch).await?;
  for (i, r) in results.iter().enumerate() {
    if let Some(c) = r.choices.first() { /* println!("{}: {}", i, c.message_text()); */ }
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
// let models = client.list_models().await?;
// for m in models { println!("{}", m.name); }
```

## Notes

Tips:

- Check docs.rs for any renames (e.g. `chat` vs `chat_completion`).
- Collect streaming deltas into a `String` if you need the final answer.
- Batch + streaming together? Launch multiple `chat_completion_stream` tasks and aggregate.
- More patterns: [Advanced Examples](/docs/advanced-examples)
