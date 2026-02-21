---
title: Python 快速开始
description: 数分钟内上手 ai-lib-python。
---

# Python 快速开始

## 安装

```bash
# Basic installation (v0.7.4+)
pip install ai-lib-python>=0.7.4

# With all optional features (recommended)
pip install ai-lib-python[full]>=0.7.4

# With specific extras (vision, audio, embeddings, structured, batch, agentic, telemetry, tokenizer)
pip install ai-lib-python[telemetry]
```

## 设置 API 密钥

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## 基础聊天

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

## 流式

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

## 工具调用

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

## 多轮对话

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

## 带统计信息

```python
response, stats = await client.chat() \
    .user("Hello!") \
    .execute_with_stats()

print(f"Content: {response.content}")
print(f"Tokens: {stats.total_tokens}")
print(f"Latency: {stats.latency_ms}ms")
```

## 切换提供商

```python
# Same API, different providers — just change the string
client = await AiClient.create("openai/gpt-4o")
client = await AiClient.create("anthropic/claude-3-5-sonnet")
client = await AiClient.create("deepseek/deepseek-chat")
client = await AiClient.create("gemini/gemini-2.0-flash")
client = await AiClient.create("qwen/qwen-plus")
```

## 下一步

- **[AiClient API](/python/client/)** — 完整 API 参考
- **[流式管道](/python/streaming/)** — 流式工作原理
- **[弹性](/python/resilience/)** — 熔断器、速率限制
- **[高级功能](/python/advanced/)** — Telemetry、路由、插件
