---
title: Python Quick Start
description: Get up and running with ai-lib-python in minutes.
---

# Python Quick Start

## Installation

```bash
# Basic installation (v0.6.0+)
pip install ai-lib-python>=0.6.0

# With all optional features (recommended)
pip install ai-lib-python[full]>=0.6.0

# With specific extras (vision, audio, embeddings, structured, batch, agentic, telemetry, tokenizer)
pip install ai-lib-python[telemetry]
```

## Set API Key

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## Basic Chat

```python
import asyncio
from ai_lib_python import AiClient

async def main():
    client = await AiClient.create("deepseek/deepseek-chat")

    response = await client.chat() \
        .user("Explain quantum computing in simple terms") \
        .temperature(0.7) \
        .max_tokens(500) \
        .execute()

    print(response.content)

asyncio.run(main())
```

## Streaming

```python
async def stream_example():
    client = await AiClient.create("deepseek/deepseek-chat")

    async for event in client.chat() \
        .user("Write a haiku about Python") \
        .stream():
        if event.is_content_delta:
            print(event.as_content_delta.text, end="")
    print()

asyncio.run(stream_example())
```

## Tool Calling

```python
async def tool_example():
    client = await AiClient.create("openai/gpt-4o")

    weather_tool = {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }

    response = await client.chat() \
        .user("What's the weather in Tokyo?") \
        .tools([weather_tool]) \
        .execute()

    if response.tool_calls:
        for call in response.tool_calls:
            print(f"Tool: {call.name}")
            print(f"Args: {call.arguments}")

asyncio.run(tool_example())
```

## Multi-turn Conversation

```python
from ai_lib_python import AiClient, Message

async def conversation():
    client = await AiClient.create("anthropic/claude-3-5-sonnet")

    messages = [
        Message.system("You are a helpful coding assistant."),
        Message.user("What is a generator in Python?"),
    ]

    response = await client.chat() \
        .messages(messages) \
        .execute()

    print(response.content)

asyncio.run(conversation())
```

## With Statistics

```python
response, stats = await client.chat() \
    .user("Hello!") \
    .execute_with_stats()

print(f"Content: {response.content}")
print(f"Tokens: {stats.total_tokens}")
print(f"Latency: {stats.latency_ms}ms")
```

## Switching Providers

```python
# Same API, different providers — just change the string
client = await AiClient.create("openai/gpt-4o")
client = await AiClient.create("anthropic/claude-3-5-sonnet")
client = await AiClient.create("deepseek/deepseek-chat")
client = await AiClient.create("gemini/gemini-2.0-flash")
client = await AiClient.create("qwen/qwen-plus")
```

## Next Steps

- **[AiClient API](/python/client/)** — Full API reference
- **[Streaming Pipeline](/python/streaming/)** — How streaming works
- **[Resilience](/python/resilience/)** — Circuit breaker, rate limiting
- **[Advanced Features](/python/advanced/)** — Telemetry, routing, plugins
