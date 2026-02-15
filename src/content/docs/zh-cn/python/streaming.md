---
title: 流式管道（Python）
description: ai-lib-python v0.6.0 中流式管道如何工作 — 解码器、选择器、累加器与事件映射器。
---

# 流式管道

Python SDK 实现与 Rust 运行时相同的基于算子的管道架构，并适配 Python 的异步生态。

## 管道阶段

```
Raw Bytes → Decoder → Selector → Accumulator → FanOut → EventMapper → StreamingEvent
```

### 1. Decoder

将 HTTP 响应字节转换为 JSON 帧：

| Decoder Class | Provider Format |
|--------------|----------------|
| `SseDecoder` | 标准 SSE（OpenAI、Groq 等） |
| `JsonLinesDecoder` | Newline-delimited JSON |
| `AnthropicSseDecoder` | Anthropic 自定义 SSE |

解码器根据清单的 `streaming.decoder.format` 选择。

### 2. Selector

使用清单中的 JSONPath 表达式过滤 JSON 帧：

```python
# Internally, the pipeline creates selectors from manifest rules:
# match: "$.choices[0].delta.content" → emit: "PartialContentDelta"
```

使用 `jsonpath-ng` 进行 JSONPath 表达式求值。

### 3. Accumulator

将部分工具调用组装为完整调用：

```python
# Provider streams:
#   {"tool_calls": [{"index": 0, "function": {"arguments": '{"ci'}}]}
#   {"tool_calls": [{"index": 0, "function": {"arguments": 'ty":"T'}}]}
#   {"tool_calls": [{"index": 0, "function": {"arguments": 'okyo"}'}}]}
# Accumulator produces complete: {"city": "Tokyo"}
```

### 4. FanOut

对于多候选响应（`n > 1`），展开为按候选的流。

### 5. EventMapper

三种 mapper 实现：

| Mapper | Description |
|--------|-------------|
| `ProtocolEventMapper` | 使用清单的 event_map 规则（JSONPath → 事件类型） |
| `DefaultEventMapper` | 兼容 OpenAI 的提供商的回退 |
| `AnthropicEventMapper` | 处理 Anthropic 的独特事件结构 |

## 异步迭代

管道以异步迭代器形式暴露事件：

```python
async for event in client.chat().user("Hello").stream():
    if event.is_content_delta:
        text = event.as_content_delta.text
        print(text, end="")
    elif event.is_tool_call_started:
        call = event.as_tool_call_started
        print(f"\nTool: {call.name}")
    elif event.is_stream_end:
        end = event.as_stream_end
        print(f"\nFinish: {end.finish_reason}")
```

## 取消

流支持优雅取消：

```python
from ai_lib_python import CancelToken

token = CancelToken()

async for event in client.chat().user("...").stream(cancel_token=token):
    # Cancel after receiving enough content
    if total_chars > 1000:
        token.cancel()
        break
```

## 下一步

- **[弹性](/python/resilience/)** — 可靠性模式
- **[高级功能](/python/advanced/)** — Telemetry、路由、插件
