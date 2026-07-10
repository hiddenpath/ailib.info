---
title: TypeScript AiClient API
description: TypeScript AiClient の詳細な API リファレンス。
---

# AiClient API

## クライアントの作成

### 基本的な作成

```typescript
import { AiClient } from '@ailib-official/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');
```

### ビルダーパターン

```typescript
import { createClientBuilder } from '@ailib-official/ai-lib-ts';

const client = await createClientBuilder()
  .withFallbacks(['anthropic/claude-3-5-sonnet', 'deepseek/deepseek-chat'])
  .withTimeout(30000)
  .withStrictStreaming(true)
  .build('openai/gpt-4o');
```

## ChatBuilder メソッド

### messages(messages: Message[])

会話メッセージを設定します。

```typescript
const response = await client
  .chat([Message.system('You are helpful.'), Message.user('Hello!')])
  .execute();
```

### user(content: string)

単一のユーザーメッセージを素早く送ります。

```typescript
const response = await client.chat().user('What is TypeScript?').execute();
```

### temperature(value: number)

サンプリング温度を設定します（0.0〜2.0）。

```typescript
const response = await client
  .chat([Message.user('Be creative')])
  .temperature(0.9)
  .execute();
```

### maxTokens(value: number)

最大出力トークン数を設定します。

```typescript
const response = await client
  .chat([Message.user('Hi')])
  .maxTokens(500)
  .execute();
```

### tools(tools: Tool[])

ツール定義を追加します。

```typescript
const tool = Tool.define(
  'search',
  {
    type: 'object',
    properties: {
      query: { type: 'string' },
    },
    required: ['query'],
  },
  'Search the web'
);

const response = await client
  .chat([Message.user('Search for TypeScript')])
  .tools([tool])
  .execute();
```

### stream()

ストリーミングモードを有効にします。

```typescript
const stream = client
  .chat([Message.user('Tell a story')])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## 実行メソッド

### execute()

リクエストを実行し、レスポンスを返します。

```typescript
const response = await client.chat([Message.user('Hello')]).execute();

console.log(response.content);
console.log(response.toolCalls);
console.log(response.usage);
```

### executeWithStats()

実行し、タイミング統計付きのレスポンスを返します。

```typescript
const { response, stats } = await client.chat([Message.user('Hi')]).executeWithStats();

console.log('Tokens:', stats.totalTokens);
console.log('Latency:', stats.latencyMs, 'ms');
console.log('Model:', stats.model);
```

### executeStream()

ストリームとして実行します。

```typescript
const stream = client
  .chat([Message.user('Write code')])
  .stream()
  .executeStream();

for await (const event of stream) {
  // Handle events
}
```

### executeStreamWithCancel()

キャンセル対応のストリームを実行します。

```typescript
const { stream, cancelHandle } = client
  .chat([Message.user('Long task')])
  .stream()
  .executeStreamWithCancel();

// Later, from another context:
// cancelHandle.cancel();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## レスポンスオブジェクト

```typescript
interface ChatResponse {
  content: string;
  toolCalls?: ParsedToolCall[];
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  model: string;
  finishReason: TerminationReason;
}
```

## エラー処理

```typescript
import { AiLibError, StandardErrorCode, isRetryable, isFallbackable } from '@ailib-official/ai-lib-ts';

try {
  const response = await client.chat([Message.user('Hi')]).execute();
} catch (e) {
  if (e instanceof AiLibError) {
    console.log('Error code:', e.code);
    console.log('Message:', e.message);
    console.log('Retryable:', isRetryable(e.code));
    console.log('Fallbackable:', isFallbackable(e.code));
  }
}
```

## シグナル

監視用のランタイムシグナルを取得します。

```typescript
const signals = await client.signals();

console.log('Circuit breaker:', signals.circuitBreaker?.state);
console.log('Rate limiter:', signals.rateLimiter?.available);
console.log('Inflight:', signals.inflight?.inUse);
```
