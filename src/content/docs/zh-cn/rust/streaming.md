---
title: 流式管道 (Rust)
description: ai-lib-rust v0.7.1 中基于算子的流式管道详解。
---

# 流式管道

流式管道是 ai-lib-rust 的核心。它通过可组合的算子处理提供商响应，每个算子由协议配置驱动。

## 管道架构

```
Raw Bytes → Decoder → Selector → Accumulator → FanOut → EventMapper → StreamingEvent
```

每个算子是管道中的一个阶段：

### 1. Decoder

将原始字节流转换为 JSON 帧。

| Format | Description |
|--------|-------------|
| `sse` | Server-Sent Events (OpenAI, Groq, etc.) |
| `ndjson` | Newline-delimited JSON |
| `anthropic_sse` | Anthropic's custom SSE format |

解码器格式在提供商清单中指定：

```yaml
streaming:
  decoder:
    format: "sse"
    done_signal: "[DONE]"
```

### 2. Selector

使用清单 `event_map` 中定义的 JSONPath 表达式过滤 JSON 帧：

```yaml
event_map:
  - match: "$.choices[0].delta.content"
    emit: "PartialContentDelta"
```

### 3. Accumulator

有状态地组装部分工具调用。当提供商以块形式流式传输工具调用参数时，累加器将其收集为完整的工具调用：

```
PartialToolCall("get_we") → PartialToolCall("ather") → PartialToolCall("(\"Tokyo\")")
```

### 4. FanOut

处理多候选响应（当 `n > 1` 时）。将候选展开为单独的事件流。

### 5. EventMapper

最终阶段 — 将处理后的帧转换为统一的 `StreamingEvent` 类型：

- `StreamingEvent::ContentDelta` — 文本内容
- `StreamingEvent::ToolCallStarted` — 工具调用开始
- `StreamingEvent::PartialToolCall` — 工具参数块
- `StreamingEvent::StreamEnd` — 响应完成

## 协议驱动构建

管道根据提供商清单自动构建。无需手动配置：

```rust
// The pipeline is constructed internally based on the protocol manifest
let mut stream = client.chat()
    .user("Hello")
    .stream()
    .execute_stream()
    .await?;
```

运行时读取清单的 `streaming` 部分，并连接相应的解码器、选择器规则和事件映射器。

## 重试与回退算子

管道还包括弹性算子：

- **Retry** — 根据清单的重试策略重试失败的流
- **Fallback** — 失败时回退到备选提供商/模型

## 下一步

- **[弹性机制](/rust/resilience/)** — 熔断器、限流器
- **[高级功能](/rust/advanced/)** — Embeddings、缓存、batch
