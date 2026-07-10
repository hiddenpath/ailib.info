---
title: TypeScript クイックスタート
description: 数分で ai-lib-ts を使い始める。
---

# TypeScript クイックスタート

## インストール

```bash
npm install @ailib-official/ai-lib-ts
export OPENAI_API_KEY="your-key"
```

**Node 18+** が必要です。

## 基本的なチャット

```typescript
import { AiClient, Message } from '@ailib-official/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');

const response = await client
  .chat([
    Message.system('You are a helpful assistant.'),
    Message.user('Hello!'),
  ])
  .execute();

console.log(response.content);
```

## モックサーバー

```typescript
import { Message, createClientBuilder } from '@ailib-official/ai-lib-ts';

const client = await createClientBuilder()
  .withMockServer('http://localhost:4010')
  .build('openai/gpt-4o');

const response = await client.chat([Message.user('Hello!')]).execute();
```

[ai-protocol-mock](https://github.com/ailib-official/ai-protocol-mock) が必要です。パターンは `tests/integration.test.ts` を参照してください。

## ストリーミング

```typescript
const stream = client
  .chat([Message.user('Count from 1 to 5')])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## エントリポイント

- **フル SDK:** `@ailib-official/ai-lib-ts`
- **実行層のみ:** `@ailib-official/ai-lib-ts/core`（ポリシー再試行ラッパーなし）
- **ポリシー層のみ:** `@ailib-official/ai-lib-ts/contact`

## 次のステップ

- **[Client API](/ja/ts/client/)**
- **[ストリーミング](/ja/ts/streaming/)**
- **[レジリエンス](/ja/ts/resilience/)**
