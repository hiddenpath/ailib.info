---
title: Quick Start
description: Get started with AI-Lib in under 5 minutes — choose Rust or Python.
---

# Quick Start

Choose your runtime and start making AI calls in minutes.

## Prerequisites

- An API key from any supported provider (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`)
- The AI-Protocol repository (automatically fetched from GitHub if not local)

## Rust

### 1. Add the dependency

```toml
[dependencies]
ai-lib = "0.7"
tokio = { version = "1", features = ["full"] }
```

### 2. Set your API key

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Write your first program

```rust
use ai_lib_rust::{AiClient, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
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

### 4. Run

```bash
cargo run
```

## Python

### 1. Install the package

```bash
pip install ai-lib-python>=0.6.0
```

### 2. Set your API key

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Write your first script

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

### 4. Run

```bash
python main.py
```

## Switching Providers

The magic of AI-Lib: change one string to switch providers.

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

No code changes needed. The protocol manifest handles endpoint, auth, parameter mapping, and streaming format for each provider.

## Next Steps

- **[Ecosystem Architecture](/ecosystem/)** — How the pieces fit together
- **[Chat Completions Guide](/guides/chat/)** — Detailed chat API usage
- **[Function Calling](/guides/tools/)** — Tool use and function calling
- **[Rust SDK Details](/rust/overview/)** — Deep dive into Rust
- **[Python SDK Details](/python/overview/)** — Deep dive into Python
