---
title: 推理模型
description: 使用 AI-Lib 使用扩展思考与推理模型。
---

# 推理模型

部分 AI 模型支持扩展思考（思维链推理），在给出最终答案前展示推理过程。

## 支持的模型

| Model | Provider | Reasoning |
|-------|----------|-----------|
| o1, o1-mini, o3 | OpenAI | Extended thinking |
| Claude 3.5 Sonnet | Anthropic | Extended thinking |
| DeepSeek R1 | DeepSeek | Chain-of-thought |
| Gemini 2.0 Flash Thinking | Google | Thinking mode |

## 用法

推理模型通过相同 API 使用。主要区别是流式时可能发出 `ThinkingDelta` 事件：

### Rust

```rust
let mut stream = client.chat()
    .user("Solve this step by step: What is 127 * 43?")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    match event? {
        StreamingEvent::ThinkingDelta { text, .. } => {
            // Model's reasoning process
            print!("[thinking] {text}");
        }
        StreamingEvent::ContentDelta { text, .. } => {
            // Final answer
            print!("{text}");
        }
        _ => {}
    }
}
```

### Python

```python
async for event in client.chat() \
    .user("Solve this step by step: What is 127 * 43?") \
    .stream():
    if event.is_thinking_delta:
        print(f"[thinking] {event.text}", end="")
    elif event.is_content_delta:
        print(event.as_content_delta.text, end="")
```

### TypeScript

```typescript
for await (const event of client
  .chat()
  .user('Solve this step by step: What is 127 * 43?')
  .stream()) {
  if (event.isThinkingDelta) {
    process.stdout.write(`[thinking] ${event.text}`);
  } else if (event.isContentDelta) {
    process.stdout.write(event.asContentDelta.text);
  }
}
```

## 工作原理

1. 提供商清单声明 `capabilities.reasoning: true`
2. 流式解码器识别与思考相关的事件
3. EventMapper 为推理内容发出 `ThinkingDelta`
4. `ContentDelta` 事件包含最终答案

协议清单处理提供商特定的格式差异：

- **OpenAI o1**：使用内部推理 tokens
- **Anthropic Claude**：使用 `thinking` 内容块
- **DeepSeek R1**：在内容中使用 `<think>` 标签

## 提示

- 推理模型通常对复杂任务表现更好
- 会消耗更多 tokens（推理 tokens 会被计费）
- 可能限制 temperature（部分推理模型会忽略该参数）
- 并非所有提供商都支持推理 — 请检查 `capabilities.reasoning`
