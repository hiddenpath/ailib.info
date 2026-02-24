---
title: 聊天补全
description: 使用 AI-Lib 运行时跨提供商使用聊天补全的指南。
---

# 聊天补全

聊天补全是与 AI 模型交互的主要 API。两个运行时均提供统一接口，适用于 37 个提供商。

## 基本用法

### Rust

```rust
let client = AiClient::from_model("openai/gpt-4o").await?;

let response = client.chat()
    .user("Hello, world!")
    .execute()
    .await?;

println!("{}", response.content);
```

### Python

```python
client = await AiClient.create("openai/gpt-4o")

response = await client.chat() \
    .user("Hello, world!") \
    .execute()

print(response.content)
```

### TypeScript

```typescript
import { AiClient } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');

const response = await client
  .chat()
  .user('Hello, world!')
  .execute();

console.log(response.content);
```

## 消息

### 系统消息

设置模型行为：

```rust
// Rust
client.chat()
    .system("You are a helpful coding assistant. Always include code examples.")
    .user("Explain closures")
    .execute().await?;
```

```python
# Python
await client.chat() \
    .system("You are a helpful coding assistant.") \
    .user("Explain closures") \
    .execute()
```

```typescript
// TypeScript
await client
  .chat()
  .system('You are a helpful coding assistant.')
  .user('Explain closures')
  .execute();
```

### 多轮对话

传入对话历史：

```rust
// Rust
use ai_lib_rust::{Message, MessageRole};

let messages = vec![
    Message::system("You are a tutor."),
    Message::user("What is recursion?"),
    Message::assistant("Recursion is when a function calls itself..."),
    Message::user("Can you show an example?"),
];

client.chat().messages(messages).execute().await?;
```

```python
# Python
from ai_lib_python import Message

messages = [
    Message.system("You are a tutor."),
    Message.user("What is recursion?"),
    Message.assistant("Recursion is when a function calls itself..."),
    Message.user("Can you show an example?"),
]

await client.chat().messages(messages).execute()
```

```typescript
// TypeScript
import { Message } from '@hiddenpath/ai-lib-ts';

const messages = [
    Message.system('You are a tutor.'),
    Message.user('What is recursion?'),
    Message.assistant('Recursion is when a function calls itself...'),
    Message.user('Can you show an example?'),
];

await client.chat().messages(messages).execute();
```

## 参数

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | float | 随机性（0.0 = 确定性，2.0 = 创造性） |
| `max_tokens` | int | 最大响应长度 |
| `top_p` | float | 核采样（temperature 的替代） |
| `stop` | string[] | 停止生成的序列 |

```rust
// Rust
client.chat()
    .user("Write a poem")
    .temperature(0.9)
    .max_tokens(200)
    .top_p(0.95)
    .execute().await?;
```

```python
# Python
await client.chat() \
    .user("Write a poem") \
    .temperature(0.9) \
    .max_tokens(200) \
    .top_p(0.95) \
    .execute()
```

```typescript
// TypeScript
await client
  .chat()
  .user('Write a poem')
  .temperature(0.9)
  .maxTokens(200)
  .topP(0.95)
  .execute();
```

## 流式

如需实时输出，使用流式：

```rust
// Rust
let mut stream = client.chat()
    .user("Tell me a story")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    if let StreamingEvent::ContentDelta { text, .. } = event? {
        print!("{text}");
        std::io::stdout().flush()?;
    }
}
```

```python
# Python
async for event in client.chat() \
    .user("Tell me a story") \
    .stream():
    if event.is_content_delta:
        print(event.as_content_delta.text, end="", flush=True)
```

```typescript
// TypeScript
for await (const event of client.chat()
  .user('Tell me a story')
  .stream()) {
  if (event.isContentDelta) {
    process.stdout.write(event.asContentDelta.text);
  }
}
```

## 响应统计

用于成本管理的使用量跟踪：

```rust
// Rust
let (response, stats) = client.chat()
    .user("Hello")
    .execute_with_stats()
    .await?;

println!("Prompt tokens: {}", stats.prompt_tokens);
println!("Completion tokens: {}", stats.completion_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

```python
# Python
response, stats = await client.chat() \
    .user("Hello") \
    .execute_with_stats()

print(f"Tokens: {stats.total_tokens}")
print(f"Latency: {stats.latency_ms}ms")
```

```typescript
// TypeScript
const { response, stats } = await client
  .chat()
  .user('Hello')
  .executeWithStats();

console.log(`Tokens: ${stats.totalTokens}`);
console.log(`Latency: ${stats.latencyMs}ms`);
```

## 提供商切换

相同代码适用于所有提供商：

```rust
// Just change the model identifier
let client = AiClient::from_model("anthropic/claude-3-5-sonnet").await?;
let client = AiClient::from_model("deepseek/deepseek-chat").await?;
let client = AiClient::from_model("gemini/gemini-2.0-flash").await?;
```

```python
# Python - same pattern
client = await AiClient.create("anthropic/claude-3-5-sonnet")
client = await AiClient.create("deepseek/deepseek-chat")
client = await AiClient.create("gemini/gemini-2.0-flash")
```

```typescript
// TypeScript - same pattern
const client = await AiClient.new('anthropic/claude-3-5-sonnet');
const client = await AiClient.new('deepseek/deepseek-chat');
const client = await AiClient.new('gemini/gemini-2.0-flash');
```

协议清单会自动处理端点 URL、认证、参数映射与流式格式差异。
