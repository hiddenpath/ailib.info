---
title: Python 快速开始
description: 几分钟内上手 ai-lib-python。
---

# Python 快速开始

## 安装

```bash
pip install ai-lib-python

# All optional capabilities
pip install ai-lib-python[full]
```

需要 **Python 3.10+**。

## 设置 API 密钥

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## 基础聊天

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

也可使用流畅简写：`client.chat().system("...").user("...").execute()`。

仓库中的同款示例：`python examples/basic_chat.py`。

## 流式处理

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

使用 `event.is_content_delta` / `event.as_content_delta.content` — 不要在包装对象上直接读 `event.content`。

## 工具调用

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

## 多轮对话

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

## 带统计信息

`ChatResponse` 不包含统计。请使用 `execute_with_stats()`：

```python
response, stats = await client.chat().user("Hello!").execute_with_stats()

print(f"Content: {response.content}")
print(f"Tokens in/out: {stats.input_tokens}, {stats.output_tokens}")
print(f"Latency: {stats.latency_ms}ms")
```

## 生产韧性（按需启用）

```python
client = await (
    AiClient.builder()
    .model("deepseek/deepseek-chat")
    .production_ready()
    .build()
)
```

## 切换提供商

```python
client = await AiClient.create("openai/gpt-4o")
client = await AiClient.create("anthropic/claude-3-5-sonnet")
client = await AiClient.create("deepseek/deepseek-chat")
client = await AiClient.create("gemini/gemini-2.0-flash")
```

## 下一步

- **[AiClient API](/zh-cn/python/client/)** — 完整 API 参考
- **[流式 Pipeline](/zh-cn/python/streaming/)** — 流式处理原理
- **[韧性模式](/zh-cn/python/resilience/)** — 熔断、限流
- **[高级功能](/zh-cn/python/advanced/)** — 遥测、路由、插件
