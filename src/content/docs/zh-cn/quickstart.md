---
title: 快速入门
description: 5 分钟内开始使用 AI-Lib —— 选择 Rust 或 Python。
---

# 快速入门

选择您的运行时，几分钟内即可开始发起 AI 调用。

## 前置条件

- 任意支持供应商的 API 密钥（如 `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`DEEPSEEK_API_KEY`）
- AI-Protocol 仓库（若无本地副本，会自动从 GitHub 拉取）

## Rust

### 1. 添加依赖

```toml
[dependencies]
ai-lib = "0.7"
tokio = { version = "1", features = ["full"] }
```

### 2. 设置 API 密钥

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. 编写第一个程序

```rust
use ai_lib::{AiClient, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    // Create client — protocol manifest is loaded automatically
    let client = AiClient::new("anthropic/claude-3-5-sonnet").await?;

    // Streaming chat
    let mut stream = client.chat()
        .user("What is AI-Protocol?")
        .temperature(0.7)
        .max_tokens(500)
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

### 4. 运行

```bash
cargo run
```

## Python

### 1. 安装包

```bash
pip install ai-lib-python>=0.6.0
```

### 2. 设置 API 密钥

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. 编写第一个脚本

```python
import asyncio
from ai_lib_python import AiClient

async def main():
    # Create client — protocol manifest loaded automatically
    client = await AiClient.create("anthropic/claude-3-5-sonnet")

    # Streaming chat
    async for event in client.chat() \
        .user("What is AI-Protocol?") \
        .temperature(0.7) \
        .max_tokens(500) \
        .stream():
        if event.is_content_delta:
            print(event.as_content_delta.text, end="")
    print()

asyncio.run(main())
```

### 4. 运行

```bash
python main.py
```

## 切换供应商

AI-Lib 的魔力：只需修改一个字符串即可切换供应商。

```rust
// Rust — just change the model ID
let client = AiClient::new("openai/gpt-4o").await?;
let client = AiClient::new("deepseek/deepseek-chat").await?;
let client = AiClient::new("gemini/gemini-2.0-flash").await?;
```

```python
# Python — same thing
client = await AiClient.create("openai/gpt-4o")
client = await AiClient.create("deepseek/deepseek-chat")
client = await AiClient.create("gemini/gemini-2.0-flash")
```

无需修改代码。协议清单会处理每个供应商的端点、认证、参数映射和流式格式。

## 下一步

- **[生态系统架构](/ecosystem/)** — 各组件如何协同工作
- **[Chat Completions 指南](/guides/chat/)** — 详细聊天 API 用法
- **[函数调用](/guides/tools/)** — 工具使用与函数调用
- **[Rust SDK 详解](/rust/overview/)** — 深入 Rust
- **[Python SDK 详解](/python/overview/)** — 深入 Python
