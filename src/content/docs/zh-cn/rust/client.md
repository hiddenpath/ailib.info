---
title: AiClient API (Rust)
description: ai-lib-rust v0.7.1 中使用 AiClient、ChatRequestBuilder 及响应类型的详细指南。
---

# AiClient API

## 创建客户端

### 通过模型标识符

```rust
// Automatic protocol loading
let client = AiClient::from_model("anthropic/claude-3-5-sonnet").await?;
```

### 使用 Builder

```rust
let client = AiClient::builder()
    .model("openai/gpt-4o")
    .protocol_dir("./ai-protocol")
    .timeout(Duration::from_secs(60))
    .build()
    .await?;
```

## ChatRequestBuilder

构建器模式提供流畅的 API：

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

## 响应类型

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

## 执行模式

### 非流式

```rust
// Simple response
let response = client.chat().user("Hello").execute().await?;

// Response with statistics
let (response, stats) = client.chat().user("Hello").execute_with_stats().await?;
```

### 流式

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

### 流式取消

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

## 错误处理

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

所有错误通过 `ErrorContext` 携带 V2 标准错误码。使用 `error.context().standard_code` 访问 `StandardErrorCode` 枚举（E1001–E9999），以便进行编程式处理。

## 批量操作

并行执行多个聊天请求：

```rust
// Execute multiple chat requests in parallel
let results = client.chat_batch(requests, 5).await; // concurrency limit = 5

// Smart batching with automatic concurrency tuning
let results = client.chat_batch_smart(requests).await;
```

## 请求验证

在发送前根据协议清单验证请求：

```rust
// Validate a request against the protocol manifest before sending
client.validate_request(&request)?;
```

## 反馈与可观测性

上报 RLHF 和监控的反馈事件，并查看弹性状态：

```rust
// Report feedback events for RLHF / monitoring
client.report_feedback(FeedbackEvent::Rating(RatingFeedback {
    request_id: "req-123".into(),
    rating: 5,
    max_rating: 5,
    category: None,
    comment: Some("Great response".into()),
    timestamp: chrono::Utc::now(),
})).await?;

// Get current resilience state
let signals = client.signals().await;
println!("Circuit: {:?}", signals.circuit_breaker);
```

## 构建器配置

使用 `AiClientBuilder` 进行高级配置：

```rust
let client = AiClientBuilder::new()
    .protocol_path("path/to/protocols".into())
    .hot_reload(true)
    .with_fallbacks(vec!["openai/gpt-4o".into()])
    .feedback_sink(my_sink)
    .max_inflight(10)
    .circuit_breaker_default()
    .rate_limit_rps(5.0)
    .base_url_override("https://my-proxy.example.com")
    .build("anthropic/claude-3-5-sonnet")
    .await?;
```

## 下一步

- **[流式管道](/rust/streaming/)** — 管道如何处理流
- **[弹性机制](/rust/resilience/)** — 可靠性模式
- **[高级功能](/rust/advanced/)** — Embeddings、缓存、插件
