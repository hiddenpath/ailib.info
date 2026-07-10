---
title: Rust 快速开始
description: 几分钟内上手 ai-lib-rust 1.0.1。
---

# Rust 快速开始

以下示例与仓库中的 [`basic_usage`](https://github.com/ailib-official/ai-lib-rust/blob/main/crates/ai-lib-rust/examples/basic_usage.rs) 一致。

## 安装

```toml
[dependencies]
ai-lib-rust = "1.0.1"
tokio = { version = "1", features = ["full"] }
futures = "0.3"   # only needed for streaming
```

可选能力：

```toml
ai-lib-rust = { version = "1.0.1", features = ["embeddings", "telemetry"] }
# or features = ["full"]
```

## API 密钥

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## 基础聊天

```rust
use ai_lib_rust::{AiClient, Message};

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("deepseek/deepseek-chat").await?;

    let response = client
        .chat()
        .messages(vec![
            Message::system("You are a helpful assistant."),
            Message::user("Explain quantum computing in simple terms."),
        ])
        .temperature(0.7)
        .max_tokens(500)
        .execute()
        .await?;

    println!("{}", response.content);
    Ok(())
}
```

## 流式处理

事件变体为 **`PartialContentDelta`**（不是 `ContentDelta`）：

```rust
use ai_lib_rust::{AiClient, Message, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("deepseek/deepseek-chat").await?;

    let mut stream = client
        .chat()
        .messages(vec![Message::user("Write a haiku about Rust.")])
        .stream()
        .execute_stream()
        .await?;

    while let Some(event) = stream.next().await {
        match event? {
            StreamingEvent::PartialContentDelta { content, .. } => print!("{content}"),
            StreamingEvent::StreamEnd { .. } => break,
            _ => {}
        }
    }
    Ok(())
}
```

## 工具调用（流式）

```rust
use ai_lib_rust::{AiClient, Message, StreamingEvent, ToolDefinition};
use futures::StreamExt;
use serde_json::json;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("openai/gpt-4o").await?;

    let weather_tool = ToolDefinition {
        name: "get_weather".into(),
        description: Some("Get current weather".into()),
        parameters: json!({
            "type": "object",
            "properties": { "city": { "type": "string" } },
            "required": ["city"]
        }),
    };

    let mut stream = client
        .chat()
        .messages(vec![Message::user("What's the weather in Tokyo?")])
        .tools(vec![weather_tool])
        .stream()
        .execute_stream()
        .await?;

    while let Some(event) = stream.next().await {
        match event? {
            StreamingEvent::ToolCallStarted { tool_name, .. } => {
                println!("Calling: {tool_name}");
            }
            StreamingEvent::PartialToolCall { arguments, .. } => print!("{arguments}"),
            StreamingEvent::PartialContentDelta { content, .. } => print!("{content}"),
            _ => {}
        }
    }
    Ok(())
}
```

## 跨任务共享 `AiClient`

```rust
use ai_lib_rust::AiClient;
use std::sync::Arc;

let client = Arc::new(AiClient::new("openai/gpt-4o").await?);
```

## 协议清单

设置本地 [ai-protocol](https://github.com/ailib-official/ai-protocol) 检出路径：

```bash
export AI_PROTOCOL_DIR="/path/to/ai-protocol"
```

或在代码中传入基路径：

```rust
use ai_lib_rust::protocol::ProtocolLoader;

let loader = ProtocolLoader::new().with_base_path("./ai-protocol");
let manifest = loader.load_provider("openai").await?;
```

## 运行附带示例

```bash
cd ai-lib-rust
DEEPSEEK_API_KEY=your_key cargo run --example basic_usage
```

## 下一步

- **[概述](/zh-cn/rust/overview/)** — 架构与能力边界
- **[Client API](/zh-cn/rust/client/)** — builder 参考
- **[流式处理](/zh-cn/rust/streaming/)** — pipeline 算子
- **[韧性模式](/zh-cn/rust/resilience/)** — 按需策略层
