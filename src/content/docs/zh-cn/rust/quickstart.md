---
title: Rust 快速入门
description: 几分钟内上手 ai-lib-rust。
---

# Rust 快速入门

## 安装

添加到你的 `Cargo.toml`：

```toml
[dependencies]
ai-lib-rust = { version = "0.8", features = ["full"] }
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

使用 `full` 特性以启用所有功能（embeddings、batch、guardrails、tokens、telemetry、routing_mvp、interceptors）。或仅指定所需特性，例如 `features = ["embeddings", "batch"]`。

## 设置 API 密钥

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## 基础对话

```rust
use ai_lib_rust::{AiClient, Message};

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
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

## 流式输出

```rust
use ai_lib_rust::{AiClient, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
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

## 工具调用

```rust
use ai_lib_rust::{AiClient, ToolDefinition, StreamingEvent};
use serde_json::json;
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
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

## 多轮对话

```rust
use ai_lib_rust::{AiClient, Message, MessageRole};

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
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

## 获取统计信息

```rust
let (response, stats) = client.chat()
    .user("Hello!")
    .execute_with_stats()
    .await?;

println!("Content: {}", response.content);
println!("Total tokens: {}", stats.total_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

## 下一步

- **[AiClient API](/rust/client/)** — 详细 API 参考
- **[流式管道](/rust/streaming/)** — 流式处理工作原理
- **[弹性机制](/rust/resilience/)** — 熔断器、限流
- **[高级功能](/rust/advanced/)** — Embeddings、缓存、插件
