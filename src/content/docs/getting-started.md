---
title: Getting Started
group: Overview
order: 20
description: Install and run your first chat call in Rust.
---

# Getting Started

This crate gives you a unified interface to multiple AI providers using pure Rust.

## Add Dependencies

`Cargo.toml`:

```toml
[dependencies]
ai-lib = "0.2.12"
tokio = { version = "1", features = ["rt-multi-thread","macros"] }
```

## Minimal Chat Request

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::types::common::Content;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
  // Select provider
  let client = AiClient::new(Provider::Groq)?;

  // Build a request (helper constructors may exist; adjust if crate renamed them)
  let req = ChatCompletionRequest::new(
    "llama3-8b-8192".into(),
    vec![Message { role: Role::User, content: Content::Text("Explain transformers in one sentence.".into()), function_call: None }]
  );

  // Core call (assumed method name: chat_completion)
  let resp = client.chat_completion(req).await?;

  // Convenience accessor patterns vary; adapt to actual response struct
  if let Some(choice) = resp.choices.first() {
    println!("Model: {}", resp.model);
    // Suppose unified message text helper exists
    // println!("Answer: {}", choice.message_text());
  }

  Ok(())
}
```

## Environment Variables

Set provider keys as normal environment variables (e.g. `OPENAI_API_KEY`, etc.). The client will pick them up according to its provider configuration.

## Proxy (Optional)

```bash
export AI_PROXY_URL=http://proxy.example.com:8080
```

## Next Steps

- Try streaming: see [Chat & Streaming](/docs/chat)
- Explore reliability: [Reliability Overview](/docs/reliability-overview)
- Check advanced code recipes: [Recipes](/docs/recipes)
