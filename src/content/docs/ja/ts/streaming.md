---
title: TypeScript ストリーミング
description: ai-lib-ts におけるストリーミングの仕組み。
---

# ストリーミングパイプライン

## 概要

ai-lib-ts は Server-Sent Events（SSE）と型付きストリーミングイベントによる、ストリーミング優先のサポートを提供します。

## 基本的なストリーミング

```typescript
import { AiClient, Message } from '@ailib-official/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');

const stream = client
  .chat([Message.user('Tell me a story')])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## ストリーミングイベント

| イベント                 | 説明           | 主なフィールド                |
| --------------------- | --------------------- | ------------------------- |
| `PartialContentDelta` | 増分テキスト      | `content`                 |
| `ToolCallStarted`     | ツール呼び出し開始   | `toolCallId`, `name`      |
| `PartialToolCall`     | 増分ツール引数 | `toolCallId`, `arguments` |
| `StreamEnd`           | ストリーム完了      | `finishReason`            |

## イベント処理

```typescript
import { StreamingEvent } from '@ailib-official/ai-lib-ts';

for await (const event of stream) {
  switch (event.event_type) {
    case 'PartialContentDelta':
      process.stdout.write(event.content);
      break;

    case 'ToolCallStarted':
      console.log(`\nCalling tool: ${event.name}`);
      break;

    case 'PartialToolCall':
      process.stdout.write(event.arguments);
      break;

    case 'StreamEnd':
      console.log(`\nFinished: ${event.finishReason}`);
      break;
  }
}
```

## ストリームのキャンセル

```typescript
const { stream, cancelHandle } = client
  .chat([Message.user('Write a very long story...')])
  .stream()
  .executeStreamWithCancel();

// Set a timeout to cancel after 10 seconds
setTimeout(() => {
  cancelHandle.cancel();
  console.log('Stream cancelled');
}, 10000);

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## パイプラインアーキテクチャ

ストリーミングパイプラインは次の段階でイベントを処理します。

```
SSE Stream → Decoder → Selector → EventMapper → Emitter
```

### Decoder

生の SSE データを構造化イベントに解析します。

```typescript
// Automatically selects decoder based on provider
// OpenAI format, Anthropic format, etc.
```

### Selector

イベントを種類でフィルタします。

```typescript
// Only content events
// Only tool events
// All events
```

### EventMapper

プロバイダー固有のイベントを標準型に変換します。

```typescript
// Provider format → Standard StreamingEvent
```

### 手動パイプライン作成

```typescript
import { Pipeline, HttpTransport } from '@ailib-official/ai-lib-ts';

const pipeline = Pipeline.fromManifest(manifest);

const stream = transport.executeStream(request);
for await (const event of stream) {
  const mapped = pipeline.map(event);
  // Handle mapped event
}
```

## AbortSignal サポート

```typescript
const controller = new AbortController();

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);

const stream = client
  .chat([Message.user('Long task')])
  .stream()
  .executeStream({ signal: controller.signal });
```

## ベストプラクティス

1. **ストリーム内のエラーを必ず処理する**

```typescript
try {
  for await (const event of stream) {
    // Handle event
  }
} catch (e) {
  console.error('Stream error:', e);
}
```

2. **ユーザー主導の停止にはキャンセルを使う**

```typescript
// UI: user clicks "Stop" button
cancelHandle.cancel();
```

3. **レート制限のためにバッファする**

```typescript
let buffer = '';
for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    buffer += event.content;
  }
}
```
