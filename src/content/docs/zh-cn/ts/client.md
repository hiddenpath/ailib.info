---
title: TypeScript AiClient API
description: TypeScript AiClient 详细 API 参考。
---

# AiClient API

## 创建客户端

### 基本创建

```typescript
import { AiClient } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');
```

### 使用构建器模式

```typescript
import { createClientBuilder } from '@hiddenpath/ai-lib-ts';

const client = await createClientBuilder()
  .withFallbacks(['anthropic/claude-3-5-sonnet', 'deepseek/deepseek-chat'])
  .withTimeout(30000)
  .withStrictStreaming(true)
  .build('openai/gpt-4o');
```

## ChatBuilder 方法

### messages(messages: Message[])

设置对话消息：

```typescript
const response = await client
  .chat([
    Message.system('你是一个有帮助的助手。'),
    Message.user('你好！'),
  ])
  .execute();
```

### user(content: string)

快速单条用户消息：

```typescript
const response = await client
  .chat()
  .user('TypeScript 是什么？')
  .execute();
```

### temperature(value: number)

设置采样温度 (0.0 - 2.0)：

```typescript
const response = await client
  .chat([Message.user('发挥创意')])
  .temperature(0.9)
  .execute();
```

### maxTokens(value: number)

设置最大输出 Token 数：

```typescript
const response = await client
  .chat([Message.user('嗨')])
  .maxTokens(500)
  .execute();
```

### tools(tools: Tool[])

添加工具定义：

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
  '搜索网络'
);

const response = await client
  .chat([Message.user('搜索 TypeScript')])
  .tools([tool])
  .execute();
```

### stream()

启用流式模式：

```typescript
const stream = client
  .chat([Message.user('讲个故事')])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## 执行方法

### execute()

执行请求并返回响应：

```typescript
const response = await client
  .chat([Message.user('你好')])
  .execute();

console.log(response.content);
console.log(response.toolCalls);
console.log(response.usage);
```

### executeWithStats()

执行并返回响应和计时统计：

```typescript
const { response, stats } = await client
  .chat([Message.user('嗨')])
  .executeWithStats();

console.log('Token 数:', stats.totalTokens);
console.log('延迟:', stats.latencyMs, 'ms');
console.log('模型:', stats.model);
```

### executeStreamWithCancel()

执行带取消支持的流：

```typescript
const { stream, cancelHandle } = client
  .chat([Message.user('长任务')])
  .stream()
  .executeStreamWithCancel();

// 稍后，从其他上下文：
// cancelHandle.cancel();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## 错误处理

```typescript
import { AiLibError, StandardErrorCode, isRetryable, isFallbackable } from '@hiddenpath/ai-lib-ts';

try {
  const response = await client.chat([Message.user('Hi')]).execute();
} catch (e) {
  if (e instanceof AiLibError) {
    console.log('错误码:', e.code);
    console.log('消息:', e.message);
    console.log('可重试:', isRetryable(e.code));
    console.log('可回退:', isFallbackable(e.code));
  }
}
```
