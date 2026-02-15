---
title: Python クイックスタート
description: 数分で ai-lib-python を始められます。
---

# Python クイックスタート

## インストール

```bash
# 基本インストール（v0.6.0+）
pip install ai-lib-python>=0.6.0

# すべてのオプション機能付き（推奨）
pip install ai-lib-python[full]>=0.6.0

# 特定の extra 付き（vision、audio、embeddings、structured、batch、agentic、telemetry、tokenizer）
pip install ai-lib-python[telemetry]
```

## API キーを設定する

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## 基本チャット

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

## ストリーミング

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

## ツール呼び出し

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

## マルチターン会話

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

## 統計付き

```python
response, stats = await client.chat() \
    .user("Hello!") \
    .execute_with_stats()

print(f"Content: {response.content}")
print(f"Tokens: {stats.total_tokens}")
print(f"Latency: {stats.latency_ms}ms")
```

## プロバイダーの切り替え

```python
# 同じ API、異なるプロバイダー — 文字列を変更するだけ
client = await AiClient.create("openai/gpt-4o")
client = await AiClient.create("anthropic/claude-3-5-sonnet")
client = await AiClient.create("deepseek/deepseek-chat")
client = await AiClient.create("gemini/gemini-2.0-flash")
client = await AiClient.create("qwen/qwen-plus")
```

## 次のステップ

- **[AiClient API](/python/client/)** — 完全な API リファレンス
- **[ストリーミングパイプライン](/python/streaming/)** — ストリーミングの仕組み
- **[耐障害性](/python/resilience/)** — サーキットブレーカー、レート制限
- **[高度な機能](/python/advanced/)** — テレメトリ、ルーティング、プラグイン
