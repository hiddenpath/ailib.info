---
title: Advanced Examples
group: Guide
order: 95
status: partial
description: Batch, cancellation, metrics, reliability, provider switching examples.
---

# Advanced Examples

Practical patterns combining the core APIs. Replace method names if your version differs.

## 1. Cancellation with Timeout (Streaming)

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::types::common::Content;
use futures_util::StreamExt;
use tokio::time::{timeout, Duration};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::OpenAI)?;
    let req = ChatCompletionRequest::new(
        "gpt-4o".into(),
        vec![Message { role: Role::User, content: Content::Text("Write a long poem about Rust lifetimes".into()), function_call: None }]
    );
    let (mut stream, handle) = client.chat_completion_stream_with_cancel(req).await?;
    let res = timeout(Duration::from_millis(500), async {
        let mut out = String::new();
        while let Some(chunk) = stream.next().await {
            if let Ok(c) = chunk { /* out.push_str(c.delta_text()); */ }
        }
        out
    }).await;
    if res.is_err() { handle.cancel(); eprintln!("Timed out and cancelled"); }
    Ok(())
}
```

## 2. Parallel Batch with Join + Simple Aggregation

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::types::common::Content;
use tokio::task;

fn prompt(q: &str) -> ChatCompletionRequest {
    ChatCompletionRequest::new(
        "gpt-4o".into(),
        vec![Message { role: Role::User, content: Content::Text(q.into()), function_call: None }]
    )
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::OpenAI)?;
    let questions = ["RAII?", "Lifetimes?", "Send vs Sync?"];
    let mut handles = Vec::new();
    for q in questions { 
        let c = client.clone(); // assuming Clone implemented
        let req = prompt(q);
        handles.push(task::spawn(async move { c.chat_completion(req).await }));
    }
    for h in handles { let _ = h.await?; }
    Ok(())
}
```

## 3. Fallback (Pseudocode)

```rust
// let chain = FallbackChain::new()
//   .primary("gpt-4o")
//   .on_timeout("claude-3-haiku")
//   .always("mistral-medium");
// let client = AiClient::builder(Provider::OpenAI).fallback(chain).build()?;
```

## 4. Race / Hedging

```rust
// let race = RacePolicy::new()
//   .contender("gpt-4o", Duration::from_millis(0))
//   .contender("claude-3-haiku", Duration::from_millis(120))
//   .cancel_others(true);
// let client = AiClient::builder(Provider::OpenAI).race(race).build()?;
```

## 5. Provider Switching + Model Listing

```rust
use ai_lib::{AiClient, Provider};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let groq = AiClient::new(Provider::Groq)?;
    let openai = AiClient::new(Provider::OpenAI)?;
    // let models = openai.list_models().await?; // iterate & pick
    // println!("OpenAI models: {}", models.len());
    // let text = groq.quick_chat_text("llama3-8b-8192", "Hi from Groq").await?;
    // println!("Groq: {text}");
    Ok(())
}
```

## 6. Metrics Integration (Skeleton)

```rust
use ai_lib::{AiClient, Provider};
use ai_lib::metrics::{Metrics, Timer};
use std::time::Instant;

struct MyMetrics;
impl Metrics for MyMetrics {
    fn incr(&self, name: &str, v: u64) { println!("METRIC {} += {}", name, v); }
    fn timer(&self, name: &str) -> Box<dyn Timer> { Box::new(MyTimer { start: Instant::now(), name: name.to_string() }) }
}
struct MyTimer { start: Instant, name: String }
impl Timer for MyTimer { fn stop(&mut self) { let d = self.start.elapsed(); println!("TIMER {} {}ms", self.name, d.as_millis()); } }

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let metrics = MyMetrics;
    let client = AiClient::new_with_metrics(Provider::OpenAI, metrics)?; // assumed constructor
    // let resp = client.quick_chat_text("gpt-4o", "Instrumented call").await?;
    Ok(())
}
```

## 7. Smart Batch (If Provided)

```rust
// let reqs = vec![ ... ];
// let results = client.chat_completion_batch_smart(reqs).await?;
```

## 8. Timeout Wrapper

```rust
use tokio::time::{timeout, Duration};
// let fut = client.chat_completion(req);
// match timeout(Duration::from_secs(3), fut).await {
//   Ok(Ok(r)) => {/* success */}
//   Ok(Err(e)) => {/* model error */}
//   Err(_) => {/* timed out */}
// }
```

## 9. Aggregating Streaming into Final String

```rust
// let mut stream = client.chat_completion_stream(req).await?;
// let mut answer = String::new();
// while let Some(chunk) = stream.next().await { if let Ok(c) = chunk { /* answer.push_str(c.delta_text()); */ } }
// println!("Final: {answer}");
```

## 10. Structured Tool Call Loop (Forward Looking)

See [Functions & Tools](/docs/functions) for a loop that detects function/tool intents, executes locally, then continues the conversation.

---

Update this page if method names change or new primitives (circuit breaker, adaptive routing) move from partial → stable.
