---
title: Rust クイックスタート
description: 数分で ai-lib-rust を始められます。
---

# Rust クイックスタート

## インストール

`Cargo.toml` に追加します：

```toml
[dependencies]
ai-lib = { version = "0.7", features = ["full"] }
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

すべての機能（embeddings、batch、guardrails、tokens、telemetry、routing_mvp、interceptors）を有効にするには `full` フィーチャーを使用します。または必要な機能のみ指定します（例：`features = ["embeddings", "batch"]`）。

## API キーを設定する

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## 基本チャット

```rust
use ai_lib::{AiClient, Message};

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    let client = AiClient::new("deepseek/deepseek-chat").await?;

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

## ストリーミング

```rust
use ai_lib::{AiClient, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    let client = AiClient::new("deepseek/deepseek-chat").await?;

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

## ツール呼び出し

```rust
use ai_lib::{AiClient, ToolDefinition, StreamingEvent};
use serde_json::json;
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    let client = AiClient::new("openai/gpt-4o").await?;

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

## マルチターン会話

```rust
use ai_lib::{AiClient, Message, MessageRole};

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    let client = AiClient::new("anthropic/claude-3-5-sonnet").await?;

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

## 統計付き

```rust
let (response, stats) = client.chat()
    .user("Hello!")
    .execute_with_stats()
    .await?;

println!("Content: {}", response.content);
println!("Total tokens: {}", stats.total_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

## 次のステップ

- **[AiClient API](/rust/client/)** — 詳細な API リファレンス
- **[ストリーミングパイプライン](/rust/streaming/)** — ストリーミングの仕組み
- **[耐障害性](/rust/resilience/)** — サーキットブレーカー、レート制限
- **[高度な機能](/rust/advanced/)** — 埋め込み、キャッシュ、プラグイン
