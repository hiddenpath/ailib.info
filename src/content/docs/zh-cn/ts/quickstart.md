---
title: TypeScript 快速开始
description: 几分钟上手 ai-lib-ts。
---

# TypeScript 快速开始

## 安装

```bash
npm install @ailib-official/ai-lib-ts
export OPENAI_API_KEY="your-key"
```

需要 **Node 18+**。

## 基础聊天

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

## Mock 服务器

```typescript
import { Message, createClientBuilder } from '@ailib-official/ai-lib-ts';

const client = await createClientBuilder()
  .withMockServer('http://localhost:4010')
  .build('openai/gpt-4o');

const response = await client.chat([Message.user('Hello!')]).execute();
```

需运行 [ai-protocol-mock](https://github.com/ailib-official/ai-protocol-mock)。

## 流式响应

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

## 下一步

- [Client API](/zh-cn/ts/client/)
- [流式处理](/zh-cn/ts/streaming/)
- [韧性模式](/zh-cn/ts/resilience/)
