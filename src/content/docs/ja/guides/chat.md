---
title: チャット補完
description: AI-Lib ランタイムでプロバイダーをまたいでチャット補完を使用するガイド。
---

# チャット補完

チャット補完は AI モデルとやり取りする主要な API です。両ランタイムは 35 以上のプロバイダーすべてで動作する統一インターフェースを提供します。

## 基本使用法

### Rust

```rust
let client = AiClient::new("openai/gpt-4o").await?;

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

## メッセージ

### システムメッセージ

モデルの振る舞いを設定します：

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

### マルチターン会話

会話履歴を渡します：

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

## パラメータ

| パラメータ | 型 | 説明 |
|------------|------|------|
| `temperature` | float | ランダム性（0.0 = 決定論的、2.0 = 創造的） |
| `max_tokens` | int | 最大レスポンス長 |
| `top_p` | float | ヌクレアスサンプリング（temperature の代替） |
| `stop` | string[] | 生成を停止するシーケンス |

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

## ストリーミング

リアルタイム出力にはストリーミングを使用します：

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

## レスポンス統計

コスト管理のための使用量を追跡します：

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

## プロバイダーの切り替え

同じコードがすべてのプロバイダーで動作します：

```rust
// モデル識別子を変更するだけ
let client = AiClient::new("anthropic/claude-3-5-sonnet").await?;
let client = AiClient::new("deepseek/deepseek-chat").await?;
let client = AiClient::new("gemini/gemini-2.0-flash").await?;
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

プロトコルマニフェストが、エンドポイント URL、認証、パラメータマッピング、ストリーミング形式の違いを自動的に処理します。
