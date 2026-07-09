---
title: Python Quick Start
description: Get up and running with ai-lib-python in minutes.
---

# Python Quick Start

## Installation

```bash
pip install ai-lib-python

# All optional capabilities
pip install ai-lib-python[full]
```

Requires **Python 3.10+**.

## Set API Key

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## Basic Chat

```python
import asyncio
from ai_lib_python import AiClient, Message

async def main():
    client = await AiClient.create("deepseek/deepseek-chat")

    response = await (
        client.chat()
        .messages([
            Message.system("You are a helpful assistant."),
            Message.user("Explain quantum computing in simple terms"),
        ])
        .temperature(0.7)
        .max_tokens(500)
        .execute()
    )

    print(response.content)
    await client.close()

asyncio.run(main())
```

You can also use fluent shorthands: `client.chat().system("...").user("...").execute()`.

Same example in the repo: `python examples/basic_chat.py`.

## Streaming

```python
import asyncio
from ai_lib_python import AiClient

async def stream_example():
    client = await AiClient.create("deepseek/deepseek-chat")

    async for event in client.chat().user("Write a haiku about Python").stream():
        if event.is_content_delta:
            print(event.as_content_delta.content, end="", flush=True)
        elif event.is_stream_end:
            break
    print()

    await client.close()

asyncio.run(stream_example())
```

Use `event.is_content_delta` / `event.as_content_delta.content` — not `event.content` on the wrapper.

## Tool Calling

```python
from ai_lib_python import ToolDefinition

async def tool_example():
    client = await AiClient.create("openai/gpt-4o")

    weather_tool = ToolDefinition(
        name="get_weather",
        description="Get current weather",
        parameters={
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    )

    response = await client.chat().user("What's the weather in Tokyo?").tools([weather_tool]).execute()

    for call in response.tool_calls:
        print(call.name, call.arguments)

    await client.close()
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

    response = await client.chat().messages(messages).execute()
    print(response.content)
    await client.close()
```

## With Statistics

`ChatResponse` does not include stats. Use `execute_with_stats()`:

```python
response, stats = await client.chat().user("Hello!").execute_with_stats()

print(f"Content: {response.content}")
print(f"Tokens in/out: {stats.input_tokens}, {stats.output_tokens}")
print(f"Latency: {stats.latency_ms}ms")
```

## Production resilience (opt-in)

```python
client = await (
    AiClient.builder()
    .model("deepseek/deepseek-chat")
    .production_ready()
    .build()
)
```

## Switching Providers

```python
client = await AiClient.create("openai/gpt-4o")
client = await AiClient.create("anthropic/claude-3-5-sonnet")
client = await AiClient.create("deepseek/deepseek-chat")
client = await AiClient.create("gemini/gemini-2.0-flash")
```

## Next Steps

- **[AiClient API](/python/client/)** — Full API reference
- **[Streaming Pipeline](/python/streaming/)** — How streaming works
- **[Resilience](/python/resilience/)** — Circuit breaker, rate limiting
- **[Advanced Features](/python/advanced/)** — Telemetry, routing, plugins
